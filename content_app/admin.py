from django.contrib import admin
from django.http import HttpResponse
from .models import Video
from import_export import resources
from django.conf import settings
import os
import json
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class VideoResource(resources.ModelResource):

    class Meta:
        model=Video

    def export_video_data_to_json(self):
        dataset=self.export()
        data = json.loads(dataset.json)

        backup_dir = os.path.join(settings.BASE_DIR, "backup/videos")
        os.makedirs(backup_dir, exist_ok=True)

        file_path = os.path.join(backup_dir, "videos.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return file_path

        
@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    actions = ["export_videos_to_json"]

    def export_videos_to_json(self, request, queryset):
        resource = VideoResource()
        file_path = resource.export_video_data_to_json()

        self.message_user(request, f"Export erfolgreich! Datei gespeichert unter: {file_path}")

    export_videos_to_json.short_description = "Videos als JSON exportieren"

