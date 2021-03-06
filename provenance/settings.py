"""
Django settings for provenance project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import logger
import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Set defaults (just for having something to start with):
s = {}
s['debug'] = True
s['key'] = 'f&jgof7m4jt-k$*=kzmlahb(w@+9d(7!245ivo5h3o=8loqf!)'
s['allowed_hosts'] = ['127.0.0.1', 'localhost']
s['static_url'] = '/static/'


# Read values from a secret file, for use in production server environment
# and overwrite the previously set values
import yaml
try:
    with open(os.path.join(BASE_DIR,'custom_settings.yaml'), 'r') as f:
        customsettings = yaml.load(f)
except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)
    raise
except yaml.YAMLError as e:
    print "Error reading YAML file: ", e
    raise
except:
    print "Unexpected error: ", sys.exc_info()[0]
    raise

# Overwrite with values read from file, if values exist:
for key in customsettings:
    s[key] = customsettings[key]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = s['key']

DEBUG = s['debug']

# Set allowed hosts, important when deploying on another host!
ALLOWED_HOSTS = s['allowed_hosts']


# Application definition
INSTALLED_APPS = [
    'core.apps.CoreConfig',
    'prov_vo.apps.ProvVoConfig',
    'prov_w3c.apps.ProvW3CConfig',
    'prov_simdm.apps.ProvSimdmConfig',
    #'floppyforms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'provenance.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.csrf',
                'core.context_processors.last_revision_date'
            ],
        },
    },
]

WSGI_APPLICATION = 'provenance.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Logging setup

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log')
        }
    },
    'loggers': {
        'core': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'prov_vo': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'prov_w3c': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'prov_simdm': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False #True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR,'static/')
STATIC_URL = s['static_url']
