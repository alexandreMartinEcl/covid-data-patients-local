"""
Copyright (c) 2020 Magic LEMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Django settings for server project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from django.utils.translation import ugettext_lazy as _

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")


SERVER_VERSION = os.getenv("VERSION").lower()
# SECURITY WARNING: don't run with debug turned on in production!


DEBUG = bool(int(os.getenv("DEBUG", '0')))


if SERVER_VERSION.lower() == "dev":
    ALLOWED_HOSTS = ["localhost", os.getenv("SERVER_IP")]


elif SERVER_VERSION.lower() == "prod":
    ALLOWED_HOSTS = ['covid-data.fr', 'covid-data.eu',
                     "www.covid-data.fr", "www.covid-data.eu",
                     os.getenv("SERVER_IP")]


# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'psycopg2',
    "users",
    "patients",
    "maj",
    "web",
    "beds",
    'bootstrap4'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


# Deasactivate user auto creation
# ACCOUNT_ADAPTER = 'server.account_adapter.NoNewUsersAccountAdapter'
ACCOUNT_ADAPTER = 'users.adapter.AuthAdapter'
SOCIALACCOUNT_PROVIDERS = {}
LOGIN_REDIRECT_URL = "http://localhost:8000"

if SERVER_VERSION == "dev":
    CORS_ORIGIN_WHITELIST = ["http://localhost:3000",
                             "http://" + os.getenv("SERVER_IP")]
    CSRF_TRUSTED_ORIGINS = ["localhost:3000", os.getenv("SERVER_IP")]

elif SERVER_VERSION == "prod":
    CORS_ORIGIN_WHITELIST = ['https://covid-data.fr',
                             'https://covid-data.eu',
                             "https://www.covid-data.fr",
                             "https://www.covid-data.eu",
                             "http://" + os.getenv("SERVER_IP")]
    CSRF_TRUSTED_ORIGINS = ['covid-data.fr', 'covid-data.eu',
                            "www.covid-data.fr", "www.covid-data.eu",
                            os.getenv("SERVER_IP")]

# CORS_ALLOW_ME"http://" + os.getenv("SERVER_IP")THODS = [
#     'GET',
#     'OPTIONS',
#     'PATCH',
#     'POST',
#     'PUT',
# ]


CORS_ALLOW_HEADERS = [
    'access-control-allow-origin',
    'content-type'
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'users.AuthMiddleware.FreeAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'rest_framework.permissions.IsAdminUser',
    # ),
}

AUTH_SERVER_URL = os.getenv("AUTH_SERVER_URL")
AUTH_SERVER_TOKEN = os.getenv("AUTH_SERVER_TOKEN")

ROOT_URLCONF = 'server.urls'


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

WSGI_APPLICATION = 'server.wsgi.application'

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases


if SERVER_VERSION == "dev":
    DATABASES = {
        'default': {
            # 'ENGINE': 'django.db.backends.sqlite3',
            # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mydb',
            'USER': 'admin',
            'PASSWORD': 'admin',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

elif SERVER_VERSION == "prod":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'mydb',
            'USER': 'admin',
            'PASSWORD': 'admin',
            'HOST': 'localhost',
            'PORT': '',
            # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
            # 'NAME': os.getenv('DTB_NAME'),
            # 'USER': os.getenv('DTB_USER'),
            # 'PASSWORD': os.getenv('DTB_PASSWORD'),
            # 'HOST': os.getenv('DTB_HOST'),
            # 'PORT': os.getenv('DTB_PORT'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

# Provide a lists of languages which your site supports.
LANGUAGES = (
    ('en', _('English')),
    ('fr', _('French')),
)
LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

REACT_APP_DIR = os.path.join(BASE_DIR, 'web', 'templates', 'beds_frontend')
STATICFILES_DIRS = [
    os.path.join(REACT_APP_DIR, 'build', 'static'),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

PROTECTED_MEDIA_ROOT = os.path.join(BASE_DIR, 'protected')
PROTECTED_MEDIA_URL = "/protected"
# PROTECTED_MEDIA_SERVER = "nginx" # Defaults to "django"
# PROTECTED_MEDIA_LOCATION_PREFIX = "/internal" # Prefix used in nginx config
# PROTECTED_MEDIA_AS_DOWNLOADS = False # Controls inclusion of a Content-Disposition header
