from django.conf import settings
from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT
# FOR LATER USE in decorator
# contains the setting of the cache total lifetime defined in settings
# CACHE_TTL = getattr(settings, 'CACHE_TTL',DEFAULT_TIMEOUT)

# Create your views here.

# Decorator for view which should be cached, needs to be added to every ENDPOINT who should be cached
# @cache_page(CACHE_TTL)
