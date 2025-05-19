import os
import pytest
from unittest import mock
from content_app import tasks

@pytest.fixture
def fake_video_path(tmp_path):
    fake_file = tmp_path / "test_video.mp4"
    fake_file.write_text("fake content") 
    return str(fake_file)

@mock.patch("content_app.tasks.subprocess.run")
@mock.patch("content_app.tasks.open", new_callable=mock.mock_open)
@mock.patch("content_app.tasks.os.makedirs")
@mock.patch("content_app.tasks.Video.objects.get")
def test_convert_to_hls_calls_ffmpeg_and_creates_master_playlist(
    mock_get_video, mock_makedirs, mock_open_file, mock_subprocess_run, fake_video_path
):
    # Mock das Video-Objekt
    mock_video_instance = mock.Mock()
    mock_get_video.return_value = mock_video_instance

    # Aufruf der Funktion mit einem Dummy-Video-ID (z.B. 1)
    tasks.convert_to_hls(fake_video_path, 1)

    # 4 Aufrufe für 4 Renditions
    assert mock_subprocess_run.call_count == 6

    # Überprüfen, ob `ffmpeg` mit korrekten Parametern aufgerufen wird (Beispiel für einen)
    called_command = mock_subprocess_run.call_args_list[0][0][0]
    assert "ffmpeg -i" in called_command
    assert "-hls_segment_filename" in called_command
    assert ".m3u8" in called_command

    # master.m3u8 wurde geschrieben
    mock_open_file.assert_called_with(
        os.path.join(fake_video_path.replace(".mp4", "") + "_hls", "master.m3u8"), "w"
    )
    handle = mock_open_file()
    handle.write.assert_any_call("#EXTM3U\n")

    # Prüfen, ob os.makedirs mehrfach aufgerufen wurde (für Renditions + Output-Ordner)
    assert mock_makedirs.call_count >= 5
