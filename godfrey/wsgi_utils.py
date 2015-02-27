# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import logging

from django.conf import settings
from django.views import debug
from django.utils import six


class BetterDebugMixin(object):
    """Provides better debugging data

    Developing API endpoints and tired of wading through HTML for HTTP
    500 errors?

    Working on POST API debugging and not seeing the POST data show up in
    the error logs/emails?

    Then this mixin is for you!

    It:

    * spits out text rather than html when DEBUG = True (OMG! THANK YOU!)
    * adds a "HTTP_X_POSTBODY" META variable so you can see the raw post data
      in error emails

    Usage:

    Create a WSGIHandler class. For example::

        import django
        from django.core.handlers.wsgi import WSGIHandler

        from godfrey.wsgi_utils import BetterDebugMixin


        class MyWSGIHandler(BetterDebugMixin, WSGIHandler):
            pass


        def get_wsgi_application()
            django.setup()
            return MyWSGIHandler()


        application = get_wsgi_application()

    """
    def handle_uncaught_exception(self, request, resolver, exc_info):
        if settings.DEBUG_PROPAGATE_EXCEPTIONS:
            raise

        logger = logging.getLogger('django.request')

        # This should be "bytes" here, though in Python 2, that's a
        # str type.
        #
        # FIXME: This is probably broken with Python 3.
        postbody = getattr(request, 'body', '')
        try:
            # For string-ish data, we truncate and encode in utf-8.
            postbody = postbody[:10000].encode('utf-8')
        except UnicodeEncodeError:
            # For binary, we say, 'BINARY CONTENT'
            postbody = 'BINARY CONTENT'

        # The logger.error generates a record which can get handled by the
        # AdminEmailHandler. Overriding all that machinery seems crazy, so
        # we're instead going to shove it in the META section.
        request.META['HTTP_X_POST_BODY'] = postbody

        logger.error('Internal Server Error: %s', request.path,
            exc_info=exc_info,
            extra={
                'status_code': 500,
                'request': request
            }
        )

        if settings.DEBUG:
            # request.is_ajax() == True will push this into doing text
            # instead of html which is waaaaaayyy more useful from an
            # API perspective. So if the Accept header is anything other
            # than html, we'll say it's an ajax request to return text.
            if 'html' not in request.META.get('HTTP_ACCEPT', 'text/html'):
                request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
            return debug.technical_500_response(request, *exc_info)

        # If Http500 handler is not installed, re-raise last exception
        if resolver.urlconf_module is None:
            six.reraise(*exc_info)

        # Return an HttpResponse that displays a friendly error message.
        callback, param_dict = resolver.resolve500()
        return callback(request, **param_dict)
