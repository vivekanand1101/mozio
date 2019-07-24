import os
import environ
from .logging_config import get_config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

root = environ.Path(__file__)
env = environ.Env(DEBUG=(bool, True), )
environ.Env.read_env()

LOGGING = get_config(env('LOG_DIR', default=BASE_DIR))

SECRET_KEY = env('SECRET_KEY', default='lol')

DEBUG = env.bool('DEBUG', default=True)

INSTALLED_APPS = ('django.contrib.admin', 'django.contrib.auth',
                  'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.messages', 'django.contrib.staticfiles',
                  'django.contrib.gis', 'rest_framework', 'rest_framework_gis',
                  'rest_framework_swagger', 'providers')

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'mozio.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mozio.wsgi.application'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': env.db(),
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = env('STATIC_ROOT')

PHONENUMBER_DB_FORMAT = 'E164'
