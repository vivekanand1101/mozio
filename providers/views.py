# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django.contrib.gis.geos import Point
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .constants import HOTSPOT_KEY_FORMAT
from .models import Providers, ServiceAreas
from .serializers import (PointSerializer, ProvidersSerializer,
                          ServiceAreasSerializer)

LOGGER = logging.getLogger(__name__)


class ProvidersViews(viewsets.ModelViewSet):
    queryset = Providers.objects
    serializer_class = ProvidersSerializer
    partial = True


class ServiceAreasViews(viewsets.ModelViewSet):

    queryset = ServiceAreas.objects
    serializer_class = ServiceAreasSerializer
    partial = True

    @list_route(url_path='search-providers')
    def search_providers(self, request):
        # First check if the point is in valid format
        point = PointSerializer(data=request.GET)
        point.is_valid(raise_exception=True)
        lat = point.data['lat']
        long = point.data['long']
        # check if it's in redis
        # we store the hotspot lat long in redis
        if settings.CACHE_ENABLED:
            data = cache.get(
                HOTSPOT_KEY_FORMAT.format(
                    lat=lat, long=long))
            if data:
                return JsonResponse(data)
        queryset = self.queryset.filter(
            polygons__intersects=Point(
                x=lat, y=long))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
