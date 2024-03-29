"""
Django settings for djbackend project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'si5y9nc(iskhxhsrwn248m6@tk%n)po^mrrmeh&1p32th1a&#5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api',
    'neo',
    'rest_framework',
    'rest_framework.authtoken',  # only if you use token authentication
    'rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.google',
    'django_extensions',
    'users',
    'pages',
    'django_ses',
    'tinymce',
    'e_mails',
    'coupons',
]

# SITE_ID = 1
#ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djbackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'static')],
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

WSGI_APPLICATION = 'djbackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#             'ENGINE': 'djongo',
#             'ENFORCE_SCHEMA': True,
#             'NAME': 'djbackend',
#             'HOST': 'localhost',
#             'PORT': 27017,
#             'USER': 'djbackend',
#             'PASSWORD': 'U&4fuAmk',
#             'AUTH_SOURCE': 'djbackend',
#             'AUTH_MECHANISM': 'SCRAM-SHA-1',
#            'REPLICASET': 'replicaset',
#            'SSL': 'ssl',
#            'SSL_CERTFILE': 'ssl_certfile',
#            'SSL_CA_CERTS': 'ssl_ca_certs',
#            'READ_PREFERENCE': 'read_preference'
#      }
# }

# DATABASES = {
#     'default': {
#             'ENGINE': 'djongo',
#             'ENFORCE_SCHEMA': True,
#             'NAME': 'djbackend',
#             'HOST': 'localhost',
#             'PORT': 27017,
#             'USER': 'localhost',
#             'PASSWORD': '',
#             'AUTH_SOURCE': 'djbackend',
#             'AUTH_MECHANISM': 'SCRAM-SHA-1',
#            'REPLICASET': 'replicaset',
#            'SSL': 'ssl',
#            'SSL_CERTFILE': 'ssl_certfile',
#            'SSL_CA_CERTS': 'ssl_ca_certs',
#            'READ_PREFERENCE': 'read_preference'
#      }
# }

DATABASES = {
        'default': {
            'ENGINE': 'djongo',
            'ENFORCE_SCHEMA': True,
            'LOGGING': {
                'version': 1,
                'loggers': {
                    'djongo': {
                        'level': 'DEBUG',
                        'propogate': False,
                    }
                },
             },
            'NAME': 'djbackend',
            'CLIENT': {
                'host': 'localhost',
                'port': 27017,
                'username': 'localhost',
                'password': '',
                'authSource': 'djbackend',
                'authMechanism': 'SCRAM-SHA-1'
            }
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = ['api.drsila.com']

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")


AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
)

REST_SESSION_LOGIN = True
EMAIL_BACKEND = 'django_ses.SESBackend'  #'django.core.mail.backends.smtp.EmailBackend'  #'django.core.mail.backends.console.EmailBackend' #'django_ses.SESBackend' #'django_smtp_ssl.SSLEmailBackend'
SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'none' #"mandatory"'optional'
ACCOUNT_EMAIL_CONFIRMATION_HMAC =False
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
#        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
   ],
    "DATE_INPUT_FORMATS": ["%d-%m-%Y"]
#Place the throttling settings here and add a comma before
}

#rest_auth_config
LOGOUT_ON_PASSWORD_CHANGE = False
ACCOUNT_LOGOUT_ON_GET = True
OLD_PASSWORD_FIELD_ENABLED = True

##custom user model
AUTH_USER_MODEL = 'users.CustomUser'



#smtp settings
#EMAIL_HOST = 'email-smtp.eu-west-1.amazonaws.com'
#EMAIL_PORT = 587 #465
#EMAIL_USE_TLS = True
#EMAIL_HOST_USER = 'AKIA3UBQWQYB3K6IPNLF'
#EMAIL_HOST_PASSWORD = 'BPXu2deT2zSE2FWfLTYzN7Fy7EFXQoktbKMwgjLTT6lR'
#EMAIL_USE_SSL = True
#EMAIL_HOST_PASSWORD = 'password from https://security.google.com/settings/security/apppasswords'
DEFAULT_FROM_EMAIL = 'accounts@drsila.com'
SERVER_EMAIL = 'accounts@drsila.com'

AWS_ACCESS_KEY_ID = 'AKIA3UBQWQYBWTKX4WA4'  #'AKIA3UBQWQYBTAZP32CQ'
AWS_SECRET_ACCESS_KEY = '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'
AWS_SES_REGION_NAME = 'eu-west-1'
AWS_SES_REGION_ENDPOINT = 'email.eu-west-1.amazonaws.com'


#tinmce editor
TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
    }
