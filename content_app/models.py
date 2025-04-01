import os
from django.db import models


# Create your models here.
class Video(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)

    def __str__(self):
        return self.title
    
