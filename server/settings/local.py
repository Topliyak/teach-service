from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
	'debug_toolbar',
]

MIDDLEWARE += [
	'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
	'127.0.0.1',
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': 'mydb.sqlite',
	},
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / 'static'

# Media files

MEDIA_ROOT = BASE_DIR / 'media'
