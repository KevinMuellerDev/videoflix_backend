from django.conf import settings
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.generics import ListAPIView
from ..models import Video
from .serializers import VideoListSerializer
from .permissions import IsAuthenticated
from django.utils.decorators import method_decorator
# FOR LATER USE in decorator
# contains the setting of the cache total lifetime defined in settings
#CACHE_TTL = getattr(settings, 'CACHE_TTL',DEFAULT_TIMEOUT)


#@method_decorator(cache_page(CACHE_TTL), name='dispatch')
class VideoListView(ListAPIView):
    queryset=Video.objects.all()
    serializer_class=VideoListSerializer
    permission_classes=[IsAuthenticated]