import os
from django.db import models


# Create your models here.
class Video(models.Model):
    GENRE_CHOICE = {
        'Action': 'Action',
        'Adventure': 'Adventure',
        'Animation': 'Animation',
        'Comedy': 'Comedy',
        'Drama': 'Drama',
        'Fantasy': 'Fantasy',
        'Horror': 'Horror',
        'Mystery': 'Mystery',
        'Romance': 'Romance',
        'Sci-Fi': 'Science Fiction',
        'Thriller': 'Thriller',
        'Documentary': 'Documentary',
        'Musical': 'Musical',
        'Western': 'Western',
        'Crime': 'Crime',
        'Biography': 'Biography',
        'Sports': 'Sports',
        'Historical': 'Historical',
    }
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=500)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    trailer = models.FileField(blank=True,null=True)
    screenshot = models.FileField(blank=True,null=True)
    genre = models.CharField(choices=GENRE_CHOICE,max_length=80)

    def __str__(self):
        return self.title
