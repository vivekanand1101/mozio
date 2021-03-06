# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Providers, ServiceAreas


class ProvidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Providers
        fields = ('id', 'name', 'email', 'phone_number', 'language',
                  'currency')


class ServiceAreasSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ServiceAreas
        fields = ('id', 'provider', 'name', 'price')
        geo_field = 'polygons'


class PointSerializer(serializers.Serializer):

    lat = serializers.FloatField()
    long = serializers.FloatField()
