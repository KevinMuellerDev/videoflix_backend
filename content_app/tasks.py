import os
import subprocess
from django.conf import settings
from django.core.cache import cache
from .models import Video


def convert_to_hls(source, video_instance_id):
    base_name = os.path.splitext(os.path.basename(source))[0]
    output_dir = os.path.splitext(source)[0] + '_hls'
    os.makedirs(output_dir, exist_ok=True)

    renditions = [
        {'name': '240p', 'scale': '426:240', 'bitrate': '400k',
            'maxrate': '450k',  'bufsize': '600k'},
        {'name': '480p', 'scale': '854:480', 'bitrate': '800k',
            'maxrate': '856k',  'bufsize': '1200k'},
        {'name': '720p', 'scale': '1280:720', 'bitrate': '1400k',
            'maxrate': '1498k', 'bufsize': '2100k'},
        {'name': '1080p', 'scale': '1920:1080', 'bitrate': '3000k',
            'maxrate': '3210k', 'bufsize': '4500k'}
    ]

    playlist_filenames = []

    for rendition in renditions:
        name = rendition['name']
        width, height = rendition['scale'].split(':')
        stream_path = os.path.join(output_dir, name)
        os.makedirs(stream_path, exist_ok=True)

        playlist_filename = f"{name}.m3u8"
        playlist_filenames.append(
            (playlist_filename, rendition['bitrate'], name))

        cmd = (
            f'ffmpeg -i "{source}" '
            f'-vf "scale=w={width}:h={height}:force_original_aspect_ratio=decrease,pad=w=ceil(iw/2)*2:h=ceil(ih/2)*2" '
            f'-c:a aac -ar 48000 -b:a 128k '
            f'-c:v h264 -profile:v main -crf 20 -sc_threshold 0 '
            f'-g 48 -keyint_min 48 '
            f'-b:v {rendition["bitrate"]} -maxrate {rendition["maxrate"]} -bufsize {rendition["bufsize"]} '
            f'-hls_time 4 -hls_playlist_type vod '
            f'-hls_segment_filename "{stream_path}/segment_%03d.ts" '
            f'"{stream_path}/{playlist_filename}"'
        )

        subprocess.run(cmd, shell=True, check=True)

    # Master playlist erstellen
    master_playlist_path = os.path.join(output_dir, 'master.m3u8')
    with open(master_playlist_path, 'w') as m3u8:
        m3u8.write('#EXTM3U\n')
        for filename, bitrate, name in playlist_filenames:
            scale = next(
                rendition for rendition in renditions if rendition['name'] == name)['scale']
            width, height = scale.split(':')
            m3u8.write(
                f'#EXT-X-STREAM-INF:BANDWIDTH={bitrate[:-1]}000,RESOLUTION={width}x{height}\n')
            m3u8.write(f'{name}/{filename}\n')

    # === Trailer erstellen (z.B. 5 Sekunden) ===
    trailer_path = os.path.join(output_dir, 'trailer.mp4')
    trailer_cmd = f'ffmpeg -y -i "{source}" -ss 00:00:05 -t 5 -c:v libx264 -c:a aac "{trailer_path}"'
    subprocess.run(trailer_cmd, shell=True, check=True)

    # === Snapshot erstellen (z.B. bei 5 Sek.) ===
    thumbnail_path = os.path.join(output_dir, 'thumbnail.jpg')
    thumbnail_cmd = f'ffmpeg -ss 00:00:01 -i "{source}" -frames:v 1 "{thumbnail_path}"'
    subprocess.run(thumbnail_cmd, shell=True, check=True)

    # Hole das Video-Objekt
    video_instance = Video.objects.get(pk=video_instance_id)

    # Relativer Pfad zur Master-Playlist
    relative_master_playlist_path = os.path.relpath(
        master_playlist_path, settings.MEDIA_ROOT)
    relative_trailer_path = os.path.relpath(trailer_path, settings.MEDIA_ROOT)
    relative_thumbnail_path = os.path.relpath(
        thumbnail_path, settings.MEDIA_ROOT)

    video_instance.video_file = relative_master_playlist_path
    video_instance.trailer = relative_trailer_path
    video_instance.screenshot = relative_thumbnail_path
    video_instance.save()
    # Löschen des Redis cache
    cache.clear()

    return master_playlist_path
