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
