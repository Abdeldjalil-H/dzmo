import os
from os.path import join
from pathlib import Path

from json import load

configs_file_path = 'dzmo_config.json' if os.getenv('DEV') else '/etc/dzmo_config.json'

with open(configs_file_path) as config_file:
    config = load(config_file)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=config.get('SECRET_KEY')
AWS_ACCESS_KEY_ID=config.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=config.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME=config.get('AWS_STORAGE_BUCKET_NAME')

AWS_S3_REGION_NAME = "eu-west-3"
AWS_S3_SIGNATURE_VERSION = "s3v4"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (config.get('DEBUG_VALUE') == 'True')
ALLOWED_HOSTS = ['algerianmo.com', 'www.algerianmo.com', 'localhost', '127.0.0.1']


#Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'lessons.apps.LessonsConfig',
    'problems.apps.ProblemsConfig',
    'accounts.apps.AccountsConfig',
    'control.apps.ControlConfig',
    'tests.apps.TestsConfig',
    'tasks.apps.TasksConfig',

    'crispy_forms',
    'mathfilters',
    'verify_email',
    'storages',
]

AUTH_USER_MODEL = 'accounts.User' #changes the default user model to ours


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dzmo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'dzmo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config.get('DB_NAME'),
        'USER': config.get('DB_USER'),
        'PASSWORD': config.get('DB_PWD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ar-DZ'

TIME_ZONE = 'Africa/Algiers'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    join(BASE_DIR, 'static')
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'


EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config.get('DEFAULT_EMAIL')
EMAIL_HOST_PASSWORD = config.get('GMAIL_KEY')#'oldoulhemzkvrsof'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = config.get('DEFAULT_EMAIL')

VERIFICATION_SUCCESS_TEMPLATE = None


LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
#Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = join(BASE_DIR, 'media')

#django_heroku.settings(locals())

AWS_S3_FILE_OVERWRITE = True
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
