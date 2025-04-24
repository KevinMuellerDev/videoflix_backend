import os
import shutil
import tempfile
from unittest import mock

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.test import override_settings

from content_app.models import Video


@pytest.mark.django_db
@mock.patch("content_app.signals.transaction.on_commit")
@mock.patch("content_app.signals.django_rq.get_queue")
def test_video_post_save_triggers_conversion(mock_get_queue, mock_on_commit):
    """
    Sicherstellen, dass convert_to_hls nach dem Erstellen eines Videos über die Queue aufgerufen wird.
    """
    queue = mock.Mock()
    mock_get_queue.return_value = queue

    video_file = SimpleUploadedFile("testvideo.mp4", b"dummy video content", content_type="video/mp4")
    video = Video.objects.create(title="Test Video", video_file=video_file)

    assert mock_on_commit.called, "transaction.on_commit wurde nicht aufgerufen"
    func = mock_on_commit.call_args[0][0]
    func()

    queue.enqueue.assert_called_once()
    args, _ = queue.enqueue.call_args
    assert video.video_file.path in args, "enqueue wurde nicht mit dem erwarteten Dateipfad aufgerufen"

@pytest.mark.django_db
@mock.patch("content_app.signals.convert_to_hls")
@mock.patch("django_rq.get_queue")  
def test_video_post_delete_removes_related_files(mock_get_queue, mock_convert_to_hls):
    """
    Sicherstellen, dass alle mit einem Video zusammenhängenden Dateien nach dem Löschen entfernt werden.
    Dabei wird kein echter RQ Worker gestartet.
    """
    tmp_dir = tempfile.mkdtemp()
    try:
        original_basename = "sample"
        video_filename = f"{original_basename}.mp4"
        video_path = os.path.join(tmp_dir, video_filename)
        with open(video_path, "wb") as f:
            f.write(b"fake content")

        related_files = [
            os.path.join(tmp_dir, f"{original_basename}_hls.m3u8"),
            os.path.join(tmp_dir, f"{original_basename}_hls_segment_001.ts"),
            os.path.join(tmp_dir, f"{original_basename}_something_else.txt"),
        ]
        for path in related_files:
            with open(path, "wb") as f:
                f.write(b"related content")

        with open(video_path, "rb") as f:
            django_file = File(f, name=video_filename)
            video = Video.objects.create(title="To Delete", video_file=django_file)

        fake_queue = mock.Mock()
        mock_get_queue.return_value = fake_queue

        video.delete()

        fake_queue.enqueue.assert_not_called()  

        for path in [video_path] + related_files:
            assert os.path.isfile(path), f"{path} sollte gelöscht worden sein"

    finally:
        
        for path in [video_path] + related_files:
            if os.path.isfile(path):
                os.remove(path)
        if os.path.isdir(tmp_dir):
            os.rmdir(tmp_dir)


