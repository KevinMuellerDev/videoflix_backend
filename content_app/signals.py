from .models import Video
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save, post_delete
import os
from .tasks import convert_to_hls
import django_rq


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('New Video created')
        queue = django_rq.get_queue('default', autocommit=True)

        transaction.on_commit(lambda: queue.enqueue(convert_to_hls, instance.video_file.path, instance.pk))


def delete_folder_contents(folder_path):
    """
    Hilfsfunktion, die alle Dateien im angegebenen Ordner löscht.
    """
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        os.rmdir(folder_path)

@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        video_dir = os.path.dirname(instance.video_file.path)

        if os.path.isdir(video_dir):
            for folder_name in os.listdir(video_dir):
                folder_path = os.path.join(video_dir, folder_name)
                # Lösche nur die Ordner, die mit der Video-Verarbeitung zu tun haben (z.B. 240p, 480p, etc.)
                if os.path.isdir(folder_path):
                    delete_folder_contents(folder_path)

        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)
        os.rmdir(video_dir)

        parent_dir=os.path.dirname(video_dir)
        last_dir = os.path.basename(video_dir)
        original_video_name = last_dir.replace('_hls','.mp4')
        original_file = os.path.join(parent_dir,original_video_name)

        os.remove(original_file)

        print(f"Alle zugehörigen Dateien und Ordner für das Video '{instance.title}' wurden gelöscht.")