# -*- coding: utf-8 -*-

import logging

from django.contrib.gis.geos import Point
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

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
        # it's valid now, get the service are queryset
        queryset = self.queryset.filter(
            polygons__intersects=Point(
                x=point.data['lat'], y=point.data['long']))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
