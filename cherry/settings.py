"""
Django settings for cherry project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cq5gmdtgfxg=)q*9$*80l4_a0gm4p9bhkbygo$94pj^$w5nn2p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

VK_ID = 4920660
VK_KEY = 'pKDM9KLbGAYJIj6S48kc'
VKONTAKTE_APP_ID = VK_ID
VKONTAKTE_APP_SECRET = VK_KEY

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cherry',
    'stdimage',
    'cart',
    'shop',
    'django_filters',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cherry.urls'

WSGI_APPLICATION = 'cherry.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#DATABASES = {
 #   'default': {
  #      'ENGINE': 'django.db.backends.sqlite3',
   #     'NAME': os.path.abspath(os.path.join(BASE_DIR, 'db.sqlite3')),
 #   }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'shop',
        'USER': 'adminJHVFe2s',
        'PASSWORD': 'CVrsAq2L3bTG',
        'HOST': os.environ['OPENSHIFT_MYSQL_DB_HOST'],
        'PORT': os.environ['OPENSHIFT_MYSQL_DB_PORT'],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

# LANGUAGE_CODE = 'en-en'
LANGUAGE_CODE = 'ru-RU'
#
LANGUAGES = [
    ('ru', 'Russian'),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(os.path.abspath(BASE_DIR), 'static')
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.environ.get('OPENSHIFT_DATA_DIR', 'media')

STATICFILES_DIRS = [
    os.path.join(os.path.abspath(BASE_DIR), 'static'),
]

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)
