import logging

import providers.urls as provider_urls
from django.conf.urls import include, url
from rest_framework import renderers, response, schemas
from rest_framework.decorators import api_view, renderer_classes
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer

LOGGER = logging.getLogger(__name__)


@api_view()
@renderer_classes(
    [SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
def api_doc(request):
    swag = schemas.SchemaGenerator(title='Mozio Provider API')
    return response.Response(swag.get_schema(request=request))


urlpatterns = [
    url(r'^$', api_doc),
    url(r'^', include(provider_urls))
]
