from .base import *
from .config import load_config
import os

config = load_config('dev.ini')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['django-secret']

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES['default'] = config['database']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = config['static-path']
STATIC_URL = '/static/'

MEDIA_ROOT = config['media-path']
MEDIA_URL = '/media/'

assert os.path.exists(STATIC_ROOT), 'Static directory doesn\'t exist: ' + STATIC_ROOT

#MIDDLEWARE.append('photosite.middleware.DebugMiddleware')

try:
    from .local import *
except ImportError:
    pass
