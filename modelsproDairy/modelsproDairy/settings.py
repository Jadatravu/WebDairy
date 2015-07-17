"""
Django settings for modelsproDairy project.

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
SECRET_KEY = '6)1v8y%3crjiqyy6rm^wnpx=^fzm537%mf4azy9a-+0a0^x&0i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
"""
TEMPLATE_LOADERS = (
   'django_jinja.loaders.AppLoader',
   'django_jinja.loaders.FileSystemLoader',
)
"""
"""
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
         }
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [ os.path.join(BASE_DIR, 'templates/jinja2'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'modelsproDairy.jinja2.environment',
        },
    },
]
"""
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/jinja2'),
            '/home/user/developer/django_1.7_py3.4/modelsproDairy/modelsapp/templates/jinja2',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'environment': 'modelsproDairy.jinja2.environment',
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]



ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'modelsapp',
)
"""
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
"""

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
"django.template.context_processors.debug",
"django.core.context_processors.csrf",
"django.template.context_processors.i18n",
"django.template.context_processors.media",
"django.template.context_processors.static",
"django.template.context_processors.tz",
"django.contrib.messages.context_processors.messages")

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


ROOT_URLCONF = 'modelsproDairy.urls'

WSGI_APPLICATION = 'modelsproDairy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/user/developer/django_1.7_py3.4/modelsproDairy/files'
MEDIA_ROOT = '/home/user/developer/django_1.7_py3.4/modelsproDairy/tmp'
MEDIA_URL = '/media/'

"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/user/developer/django_1.7_py3.4/modelsproDairy/logapp.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'simple':{
           'format':'%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'file':{
            'level':'DEBUG',
            'class':'logging.FileHandler',
            'filename':'/home/user/developer/django_1.7_py3.4/modelsproDairy/logapp.log',
            'formatter':'simple'
        },
    },
    'loggers': {
        'modelsapp':{
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
