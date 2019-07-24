# -*- coding: utf-8 -*-
import json

from django.contrib.gis.geos import MultiPolygon, Polygon
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Providers, ServiceAreas
from .serializers import ProvidersSerializer, ServiceAreasSerializer


class ProvidersViewSetTest(TestCase):
    def setUp(self):
        self.provider_obj = Providers.objects.create(
            name='vivek',
            email='vivek@anand.com',
            phone_number='+919876543210',
            language='eng',
            currency='INR')

    def test_providers_list(self):
        resp = self.client.get(reverse('providers:providers-list'))
        self.assertEqual(
            dict(resp.data[0]),
            ProvidersSerializer(self.provider_obj).data)

    def test_providers_create(self):
        resp = self.client.post(
            reverse('providers:providers-list'),
            data={
                'currency': 'INR',
                'email': 'vivek@anand.com',
                'language': 'ang',
                'name': 'vivek',
                'phone_number': '+919876543210'
            })
        self.assertEqual(
            resp.data,
            ProvidersSerializer(instance=Providers.objects.last()).data)

    def test_providers_delete(self):
        resp = self.client.delete(
            reverse(
                'providers:providers-detail',
                kwargs={'pk': self.provider_obj.pk}))
        self.assertIsNone(resp.data)
        self.assertEqual(
            list(Providers.objects.filter(pk=self.provider_obj.pk)), [])

    def test_providers_update(self):
        resp = self.client.patch(
            reverse(
                'providers:providers-detail',
                kwargs={'pk': self.provider_obj.pk}),
            data=json.dumps({'name': 'anand'}),
            content_type="application/json")
        self.assertEqual(resp.data['name'], 'anand')

    def test_providers_get(self):
        resp = self.client.get(
            reverse(
                'providers:providers-detail',
                kwargs={'pk': self.provider_obj.pk}))
        self.assertEqual(resp.data, ProvidersSerializer(self.provider_obj).data)


class ServiceAreasViewSetTest(TestCase):
    def setUp(self):
        self.provider_obj = Providers.objects.create(
            name='vivek',
            email='vivek@anand.com',
            phone_number='+919876543210',
            language='eng',
            currency='INR')
        self.service_area = ServiceAreas.objects.create(
            provider=self.provider_obj,
            name='foo',
            price='1.00',
            polygons=MultiPolygon(
                Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
                Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))))

    def test_service_areas_list(self):
        resp = self.client.get(reverse('providers:service-areas-list'))
        self.assertEqual(
            dict(resp.data['features'][0]),
            ServiceAreasSerializer(self.service_area).data)

    def test_service_areas_create(self):
        resp = self.client.post(
            reverse('providers:service-areas-list'),
            data=json.dumps({
                'provider': self.provider_obj.pk,
                'name': 'bar',
                'price': '1.00',
                'polygons': {
                    'coordinates': [[[[0.0, 0.0], [0.0, 1.0], [1.0, 1.0],
                                      [0.0, 0.0]]],
                                    [[[1.0, 1.0], [1.0, 2.0], [1.0, 2.0],
                                      [1.0, 1.0]]]],
                    'type':
                    'MultiPolygon'
                }
            }),
            content_type="application/json")
        self.assertEqual(
            resp.data,
            ServiceAreasSerializer(instance=ServiceAreas.objects.last()).data)

    def test_service_areas_search(self):
        resp = self.client.get(
            reverse('providers:service-areas-search-providers'),
            data={
                'lat': 0,
                'long': 0.5
            })
        self.assertEqual(
            dict(resp.data['features'][0]),
            ServiceAreasSerializer(self.service_area).data)
        self.assertEqual(len(resp.data['features']), 1)

    def test_service_areas_find_many(self):
        service_area = ServiceAreas.objects.create(
            provider=self.provider_obj,
            name='bar',
            price='2.00',
            polygons=MultiPolygon(
                Polygon(((0, 0), (0, 1), (1, 1), (0, 0))),
                Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))))

        resp = self.client.get(
            reverse('providers:service-areas-search-providers'),
            data={
                'lat': 0,
                'long': 0.5
            })
        self.assertEqual(
            dict(resp.data['features'][0]),
            ServiceAreasSerializer(self.service_area).data)
        self.assertEqual(
            dict(resp.data['features'][1]),
            ServiceAreasSerializer(service_area).data)
        self.assertEqual(len(resp.data['features']), 2)
