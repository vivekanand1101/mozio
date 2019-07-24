# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import ProvidersViews, ServiceAreasViews

router = DefaultRouter(schema_title='API')
router.register(r'providers', ProvidersViews, base_name='providers')
router.register(r'service-areas', ServiceAreasViews, base_name='service-areas')
api_urlpatterns = router.urls

urlpatterns = [
    url(r'^', include(api_urlpatterns, namespace='providers')),
]
