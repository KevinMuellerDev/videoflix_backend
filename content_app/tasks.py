# # tasks um hochgeladene videos zu konvertieren !
# import subprocess

# def convert_480p(source):
#     new_file_name = source.replace('.mp4', '') + '_480p.mp4'
#     cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
#     subprocess.run(cmd, shell=True)

import os
import subprocess

def convert_to_hls(source):
    base_name = os.path.splitext(os.path.basename(source))[0]
    output_dir = os.path.splitext(source)[0] + '_hls'
    os.makedirs(output_dir, exist_ok=True)

    renditions = [
        {'name': '240p', 'scale': '426:240', 'bitrate': '400k',  'maxrate': '450k',  'bufsize': '600k'},
        {'name': '480p', 'scale': '854:480', 'bitrate': '800k',  'maxrate': '856k',  'bufsize': '1200k'},
        {'name': '720p', 'scale': '1280:720','bitrate': '1400k', 'maxrate': '1498k', 'bufsize': '2100k'},
        {'name': '1080p','scale': '1920:1080','bitrate': '3000k','maxrate': '3210k', 'bufsize': '4500k'}
    ]

    playlist_filenames = []

    for rendition in renditions:
        name = rendition['name']
        stream_path = os.path.join(output_dir, name)
        os.makedirs(stream_path, exist_ok=True)

        playlist_filename = f"{name}.m3u8"
        playlist_filenames.append((playlist_filename, rendition['bitrate'], name))

        cmd = (
            f'ffmpeg -i "{source}" '
            f'-vf "scale=w={rendition["scale"].split(":")[0]}:h={rendition["scale"].split(":")[1]}:force_original_aspect_ratio=decrease" '
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
        for filename, bandwidth, name in playlist_filenames:
            m3u8.write(f'#EXT-X-STREAM-INF:BANDWIDTH={bandwidth[:-1]}000,RESOLUTION={name[:-1]}\n')
            m3u8.write(f'{name}/{filename}\n')

