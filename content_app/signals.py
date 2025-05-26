from .models import Video
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save, post_delete
import os
from .tasks import convert_to_hls
import django_rq
import shutil


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        transaction.on_commit(lambda: queue.enqueue(convert_to_hls, instance.video_file.path, instance.pk))


def delete_folder_contents(folder_path):
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

        os.rmdir(folder_path)


def delete_original_file(video_dir):
    parent_dir=os.path.dirname(video_dir)
    last_dir = os.path.basename(video_dir)
    original_video_name = last_dir.replace('_hls','.mp4')
    original_file = os.path.join(parent_dir,original_video_name)

    os.remove(original_file)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        video_dir = os.path.dirname(instance.video_file.path)

        if os.path.isdir(video_dir):
            # sicheres rekursives Löschen des gesamten Ordners
            shutil.rmtree(video_dir, ignore_errors=False)

        # Originaldatei löschen, falls noch vorhanden
        try:
            delete_original_file(video_dir=video_dir)
        except FileNotFoundError:
            pass