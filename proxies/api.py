import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework_csv.renderers import CSVRenderer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .permissions import ReadOnly
from .utils.proxies import get_proxies, proxy_was_successful
from .utils.response_headers import response_headers


class HomeAPI(APIView):
    permission_classes = (ReadOnly,)
    renderer_classes = (TemplateHTMLRenderer,)

    @method_decorator(cache_page(60*60*24*365))
    def get(self, request, *args, **kwargs):
        return Response(
            headers=response_headers,
            template_name='home.html',
            content_type='text/html',
        )

    def options(self, request, *args, **kwargs):
        if self.metadata_class is None:
            return self.http_method_not_allowed(request, *args, **kwargs)
        data = self.metadata_class().determine_metadata(request, self)
        return Response(data, template_name='empty.html', status=200)


class ProxiesAPI(APIView):
    permission_classes = (ReadOnly,)
    renderer_classes = (JSONRenderer,)

    @method_decorator(cache_page(600))
    def get(self, request, *args, **kwargs):
        try:
            proxies = get_proxies()
        except Exception as e:
            logging.error(e)
            raise e
        return Response(
            data=proxies,
            headers=response_headers,
            content_type='application/json',
        )


class CSVAPI(APIView):
    permission_classes = (ReadOnly,)
    renderer_classes = (CSVRenderer, JSONRenderer,)

    @method_decorator(cache_page(600))
    def get(self, request, *args, **kwargs):
        try:
            proxies = get_proxies()
        except Exception as e:
            logging.error(e)
            raise e

        headers = dict(response_headers)
        headers['Content-Disposition'] = 'attachment; filename=proxies.csv'

        return Response(
            data=proxies,
            headers=headers,
            content_type='text/csv',
        )


class TestedAPI(APIView):
    permission_classes = (ReadOnly,)
    renderer_classes = (JSONRenderer,)

    @method_decorator(cache_page(600))
    def get(self, request, *args, **kwargs):
        try:
            proxies = get_proxies()
        except Exception as e:
            logging.error(e)
            raise e
        
        for count, proxy in enumerate(proxies, start=1):
            try:
                tested_proxy = proxy_was_successful(proxy)
            except:
                if count == len(proxies):
                    e = APIException('Could not find workable proxy.')
                    logging.error(e)
                    raise e
                else:
                    continue
            return Response(
                data={ 'proxy': tested_proxy },
                headers=response_headers,
                content_type='application/json',
            )
