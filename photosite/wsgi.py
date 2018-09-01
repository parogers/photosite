"""
WSGI config for photosite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photosite.settings")

class DebugWrapper:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # WSGI interface is defined in PEP-3333
        # https://www.python.org/dev/peps/pep-3333/
        print(environ['REQUEST_METHOD'], environ['PATH_INFO'])
        print('Query string:', environ['QUERY_STRING'])
        print('Streams:')
        print('* wsgi.input', environ['wsgi.input'])
        print('* wsgi.errors', environ['wsgi.errors'])
        print('Headers:')
        http_headers = filter(
            lambda x : x.startswith('HTTP_'),
            environ.keys())
        for header in http_headers:
            print('*', header, environ[header])
        
        return self.app(environ, start_response)

application = get_wsgi_application()
#application = DebugWrapper(get_wsgi_application())
