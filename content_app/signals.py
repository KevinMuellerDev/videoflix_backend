from .models import Video
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
import os
from .tasks import convert_to_hls
import django_rq
import shutil


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:
        queue = django_rq.get_queue('default', autocommit=True)
        transaction.on_commit(lambda: queue.enqueue(
            convert_to_hls, instance.video_file.path, instance.pk))


def delete_original_file(video_dir):
    parent_dir = os.path.dirname(video_dir)
    last_dir = os.path.basename(video_dir)
    original_video_name = last_dir.replace('_hls', '.mp4')
    original_file = os.path.join(parent_dir, original_video_name)

    os.remove(original_file)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file:
        video_dir = os.path.dirname(instance.video_file.path)

        if os.path.isdir(video_dir):
            shutil.rmtree(video_dir, ignore_errors=False)

        try:
            delete_original_file(video_dir=video_dir)
        except FileNotFoundError:
            pass
        # Löschen des Redis cache
    cache.clear()
