from rest_framework import serializers
from ..models import Video

class VideoListSerializer(serializers.ModelSerializer):

    class Meta:
        model=Video
        fields = ['created_at','title','description','video_file','trailer','screenshot','genre']