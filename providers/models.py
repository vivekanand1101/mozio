# -*- coding: utf-8 -*-

from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from base.models import BaseModel

from .constants import CURRENCIES, LANGUAGES


class Providers(BaseModel):
    name = models.CharField(_('name'), max_length=255)
    email = models.EmailField(_('email address'), max_length=254)
    phone_number = PhoneNumberField(
        _('phone number'), help_text=_('Correct format: "+919876543210"'))
    language = models.CharField(_('language'), max_length=3, choices=LANGUAGES)
    currency = models.CharField(
        _('currency'), max_length=3, choices=CURRENCIES)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'providers'


class ServiceAreas(BaseModel):
    provider = models.ForeignKey(Providers, related_name='service_areas')
    name = models.CharField(_('name'), max_length=255)
    price = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    polygons = gis_models.MultiPolygonField(_('polygons'), spatial_index=True)

    def __str__(self):
        return '{} (provider: {}, price: {})'.format(self.name, self.provider,
                                                     self.price)

    class Meta:
        db_table = 'provider_service_areas'
