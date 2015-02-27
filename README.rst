==============
Django Godfrey
==============

Provides a WSGIHandler mixin for better handling of uncaught exceptions
particularly when working on API endpoints that use JSON payloads.

Provides a set of error views that look at the Accepts HTTP header and
return appropriately formatted responses. This way someone's API-using client
doesn't get a boatload of HTML for an HTTP 404.

:Code:          https://github.com/willkg/django-godfrey
:License:       Mozilla Public License v2; see LICENSE
:Issues:        https://github.com/willkg/django-godfrey/issues
:Documentation: None, yet--this is pretty prototypey


.. Note::

   This is very pre-alpha! I'm playing with this code to figure out the
   best way to accomplish what I need to accomplish while doing the
   least amount of hacky stuff.


Handling uncaught exceptions
============================

When ``DEBUG=True`` and an uncaught exception happens, Django will return a
stunning amount of HTML-formatted information in the HTTP Response. This
sucks when you're debugging API issues since you have to wade through the
HTML to find the information you want.

Godfrey tweaks that so that if the ``Accepts`` HTTP header includes
``application/json``, it tweaks the ``HttpRequest`` to look as if it
were an AJAX request which causes the debug info to come out as
text. I find it a lot easier to get back unformatted text because the
interfaces I'm using to test API things (e.g. curl, command line
utilities, Firefox dev tools, etc.) display that pretty well.

When ``DEBUG=False`` and an uncaught exception happens and Django is
configured to send email, Django will send an error email to the ``ADMINS``
which includes a repr of the WSGIRequest. However, when dealing with
HTTP POST payloads that are in JSON format (and probably other
formats), then the repr of the WSGIRequest doesn't show the payload at
all. It shows this::

  POST:<QueryDict {}>

or this::

  POST:<Could not parse>

Neither is helpful.

Godfrey tweaks the WSGIRequest by putting the raw POST payload in the
``HTTP_X_POSTDATA`` META variable so that it shows up in the error logs.

To use the mixin, in your ``wsgi.py`` file, do something like this::

  import django
  from django.core.handlers.wsgi import WSGIHandler

  from godfrey.wsgi_utils import BetterDebugMixin


  class MyWSGIHandler(BetterDebugMixin, WSGIHandler):
      pass


  def get_wsgi_application()
      django.setup()
      return MyWSGIHandler()


  application = get_wsgi_application()


.. Note::

   This is really hacky, but I didn't see another way to do this without
   rewriting/overriding a lot of Django error handling.

   I'm happy to entertain better ideas.

   

Error views
===========

By default, the Django error views for 400, 403, 404 and 500 all render
HTML. This sucks for API-users.

You can change the template to something different, but what you really
want is to return the appropriate format according to the HTTP ``Accepts``
header.

Godfrey has an alternative set of error handlers that will look at the
``Accepts`` header and return appropriately formatted things.

To use the views, in your url conf file, do this::

  from godfrey.error_handlers import setup_handlers()
  setup_handlers()


.. Note::

   This could use a lot of work, but I think the gist of it is good.
