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
from content_app.signals import delete_folder_contents, delete_original_file, video_post_delete


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


@pytest.fixture
def tmp_video_dir(tmp_path):
    video_dir = tmp_path / 'test_video_hls'
    video_dir.mkdir()
    (video_dir / 'file1.txt').write_text('test')
    (video_dir / 'file2.txt').write_text('test')
    return video_dir


def test_delete_folder_contents(tmp_video_dir):
    delete_folder_contents(tmp_video_dir)
    assert not os.path.exists(tmp_video_dir)


def test_delete_original_file(tmp_path):
    parent_dir = tmp_path
    video_dir = parent_dir / 'test_video_hls'
    video_dir.mkdir()
    original_file = parent_dir / 'test_video.mp4'
    original_file.touch()

    delete_original_file(video_dir)
    assert not original_file.exists()


def test_video_post_delete(tmp_video_dir):
    with patch('content_app.signals.os') as mock_os:
        mock_instance = MagicMock()
        mock_instance.video_file.path = str(tmp_video_dir / 'file1.txt')

        video_post_delete(sender=Video, instance=mock_instance)

        mock_os.path.isdir.assert_called()
        mock_os.path.isfile.assert_called()
        mock_os.remove.assert_called()
        mock_os.rmdir.assert_called()