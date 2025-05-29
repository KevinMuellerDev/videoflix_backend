import os
import shutil
import tempfile
from unittest import mock
from unittest.mock import MagicMock, patch

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
@mock.patch("content_app.signals.delete_original_file")
def test_video_post_delete_removes_video_directory(mock_delete_original_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        video_path = os.path.join(temp_dir, "test_video.mp4")
        with open(video_path, "wb") as f:
            f.write(b"dummy content")

        uploaded = SimpleUploadedFile("videos/test_video.mp4", b"dummy content", content_type="video/mp4")

        video = Video.objects.create(
            title="Test Video",
            description="Test description",
            video_file=uploaded,
            genre="Action"
        )

        video_dir = os.path.dirname(video.video_file.path)
        os.makedirs(video_dir, exist_ok=True)

        video.delete()

        assert not os.path.exists(video_dir)
        mock_delete_original_file.assert_called_once_with(video_dir=video_dir)


@pytest.mark.django_db
@mock.patch("content_app.signals.delete_original_file")
def test_video_post_delete_when_no_video_file(mock_delete_original_file):
    video = Video.objects.create(
        title="No File",
        description="No file present",
        video_file=None,
        genre="Drama"
    )
    video.delete()
    mock_delete_original_file.assert_not_called()


@pytest.mark.django_db
@mock.patch("content_app.signals.delete_original_file", side_effect=FileNotFoundError)
def test_video_post_delete_handles_missing_original_file(mock_delete_original_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        dummy_file = os.path.join(temp_dir, "test_video.mp4")
        with open(dummy_file, "wb") as f:
            f.write(b"dummy content")

        uploaded = SimpleUploadedFile("videos/test_video.mp4", b"dummy content", content_type="video/mp4")

        video = Video.objects.create(
            title="FileNotFound Test",
            description="Expecting missing file",
            video_file=uploaded,
            genre="Comedy"
        )

        video_dir = os.path.dirname(video.video_file.path)
        os.makedirs(video_dir, exist_ok=True)

        video.delete()

        mock_delete_original_file.assert_called_once_with(video_dir=video_dir)