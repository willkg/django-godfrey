# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from django.http import JsonResponse
from django.views.defaults import (
    bad_request,
    page_not_found,
    permission_denied,
    server_error
)


def handler_http_400(request, template_name='400.html'):
    """HTTP 400 error handler that understands Accept header"""

    accepts = request.META.get('HTTP_ACCEPT', 'text/html')
    if 'application/json' in accepts:
        return JsonResponse(
            status=400,
            content_type='application/json',
            data={'error': 'bad request'}
        )

    if 'text/html' in accepts:
        return bad_request(request, template_name=template_name)


def handler_http_403(request, template_name='403.html'):
    """HTTP 403 error handler that understands Accept header"""

    accepts = request.META.get('HTTP_ACCEPT', 'text/html')
    if 'application/json' in accepts:
        return JsonResponse(
            status=403,
            content_type='application/json',
            data={'error': 'permission denied'}
        )

    if 'text/html' in accepts:
        return permission_denied(request, template_name=template_name)


def handler_http_404(request, template_name='404.html'):
    """HTTP 404 error handler that understands Accept header"""

    accepts = request.META.get('HTTP_ACCEPT', 'text/html')
    if 'application/json' in accepts:
        return JsonResponse(
            status=404,
            content_type='application/json',
            data={'error': 'page not found'}
        )

    if 'text/html' in accepts:
        return page_not_found(request, template_name=template_name)


def handler_http_500(request, template_name='500.html'):
    """HTTP 500 error handler that understands Aceept header"""

    # FIXME: Figure out how to do mimetype dispatching better
    accepts = request.META.get('HTTP_ACCEPT', 'text/html')
    if 'application/json' in accepts:
        return JsonResponse(
            status=500,
            content_type='application/json',
            data={'error': 'server error'}
        )

    if 'text/html' in accepts:
        return server_error(request, template_name=template_name)


def setup_handlers():
    import django.conf.urls

    django.conf.urls.handler400 = 'godfrey.error_handlers.handler_http_400'
    django.conf.urls.handler403 = 'godfrey.error_handlers.handler_http_403'
    django.conf.urls.handler404 = 'godfrey.error_handlers.handler_http_404'
    django.conf.urls.handler500 = 'godfrey.error_handlers.handler_http_500'
