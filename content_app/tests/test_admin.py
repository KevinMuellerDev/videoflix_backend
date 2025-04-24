import pytest
from unittest import mock
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from content_app.admin import VideoAdmin, VideoResource
from content_app.models import Video
import tempfile
import os

User = get_user_model()

@pytest.mark.django_db
class TestVideoAdmin:

    @pytest.fixture
    def video(self):
        # Erstellen einer temporären Datei für das Video-Feld
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(b'Test Video Content')  # Beispielinhalt
        temp_file.close()

        video = Video.objects.create(
            title="Test Video",
            description="A sample video description.",
            video_file=temp_file.name,  # Hier setzen wir die temporäre Datei als Video-Datei
            genre="Action"
        )

        yield video

        # Aufräumen der temporären Datei nach dem Test
        os.remove(temp_file.name)

    @pytest.fixture
    def admin_user(db):
        return User.objects.create_superuser(
            email="admin@example.com",
            password="pass"
        )

    @pytest.fixture
    def admin_request(self, admin_user, rf):
        admin_request = rf.get("/")
        admin_request.user = admin_user
        return admin_request

    def test_export_video_data_to_json_mocked(self, tmp_path):
        resource = VideoResource()

        # Mock internals
        with (
            mock.patch.object(resource, "export") as mock_export,
            mock.patch("builtins.open", mock.mock_open()) as mock_file,
            mock.patch("os.makedirs") as mock_makedirs
        ):
            # Setup mocked export().json return
            mock_export.return_value.json = '[{"title": "Mock Video", "url": "https://example.com"}]'

            file_path = resource.export_video_data_to_json()

            # check file creation
            mock_export.assert_called_once()
            mock_makedirs.assert_called_once()
            mock_file.assert_called_once_with(file_path, "w", encoding="utf-8")

    def test_admin_action_message(self, admin_request, video):
        ma = VideoAdmin(Video, AdminSite())

        with (
            mock.patch.object(VideoResource, "export_video_data_to_json", return_value="/tmp/videos.json"),
            mock.patch.object(ma, "message_user") as mock_message
        ):
            ma.export_videos_to_json(admin_request, Video.objects.all())

            mock_message.assert_called_once_with(
                admin_request,
                "Export erfolgreich! Datei gespeichert unter: /tmp/videos.json"
            )


    def test_video_creation(self, video):
        """Testet die Erstellung eines Video-Objekts und ob die Werte korrekt sind"""
        
        # Erstelle eine temporäre Datei
        file_path = os.path.join('media', 'videos', 'test_video.mp4')
        file_content = b"Test video content"
        video_file = SimpleUploadedFile(name='test_video.mp4', content=file_content, content_type='video/mp4')

        video.video_file = video_file  # Weise die Datei dem Video-Objekt zu
        video.save()

        assert video.title == "Test Video"
        assert video.description == "A sample video description."
        assert video.genre == "Action"
        assert os.path.exists(video.video_file.path)  # Überprüfen, dass die Datei existiert

    def test_video_str_representation(self, video):
        """Testet die __str__ Methode des Video-Modells"""
        assert str(video) == "Test Video"
