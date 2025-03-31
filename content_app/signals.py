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
        #queue.enqueue(convert_480p,instance.video_file.path)
    
@receiver(post_delete, sender=Video)
def video_post_delete(sender,instance,**kwargs):
    #video_file ist der ort wo das model die file speichert (ist im model definiert)
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)