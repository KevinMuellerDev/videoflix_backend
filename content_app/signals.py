from .models import Video
from django.dispatch import receiver
from django.db import transaction
from django.db.models.signals import post_save,post_delete
import os
from .tasks import convert_480p
import django_rq


#sender => model
#instance => video object
#created => boolean

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video wurde gespeichert')
    if created:
        print('New Video created')
        queue = django_rq.get_queue('default',autocommit=True)
        transaction.on_commit(lambda: queue.enqueue(convert_480p, instance.video_file.path))
    
@receiver(post_delete, sender=Video)
def video_post_delete(sender,instance,**kwargs):

    if instance.video_file:
        video_dir = os.path.dirname(instance.video_file.path)
        original_video_name = os.path.basename(instance.video_file.name).split('.')[0]  # Der Name ohne Extension

        for filename in os.listdir(video_dir):
            if filename.startswith(original_video_name):
                file_path = os.path.join(video_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)