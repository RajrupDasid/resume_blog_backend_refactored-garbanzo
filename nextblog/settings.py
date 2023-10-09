from datetime import timedelta
from pathlib import Path
from decouple import config
import os
import boto3
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
AUTH_USER_MODEL = 'accounts.User'

SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if config('DEBUG') == "True" else False

PRODUCTION = True if config('PRODUCTION') == "True" else False
IS_REDIS = True if config('IS_REDIS') == "True" else False
IS_MEMCACHED = True if config('IS_MEMCACHED') == "True" else False

# Statement interface for debug
if DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        'http://localhost:3000',
        'http://127.0.0.1:8000',
    ]
    CORS_ORIGIN_WHITELIST = [
        'http://localhost:3000',
        'http://127.0.0.1:8000',

    ]
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

PRODUCTION_SITE_ONE = config("PRODUCTION_SITE")
PRODUCTION_SITE_TWO = config("PRODUCTION_SITE_TWO")

if PRODUCTION:
    CSRF_TRUSTED_ORIGINS = [
        PRODUCTION_SITE_ONE,
        PRODUCTION_SITE_TWO
    ]
    CORS_ORIGIN_WHITELIST = [
        PRODUCTION_SITE_ONE,
        PRODUCTION_SITE_TWO

    ]
    ALLOWED_HOSTS = [PRODUCTION_SITE_ONE, PRODUCTION_SITE_TWO]

# Statement interface for prodcution control

# Application definition

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'analytics.apps.AnalyticsConfig',
    'ckeditor',
    'ckeditor_uploader',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'controller.apps.ControllerConfig',
    'rest_framework',
    "rest_framework_api_key",
    'taggit',
    'storages'


]
# # channel layers
# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer',
#     },
# }

if PRODUCTION:
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.cache.UpdateCacheMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # 'analyticsapp.middlewares.TrackIPAddressMiddleware'
    ]
    CACHE_MIDDLEWARE_ALIAS = "default"
    CACHE_MIDDLEWARE_SECONDS = 600
    CACHE_MIDDLEWARE_KEY_PREFIX = "default"
else:
    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        # 'analyticsapp.middlewares.TrackIPAddressMiddleware'

    ]


ROOT_URLCONF = 'nextblog.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'nextblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('SUPABASE_DB_NAME'),
            'HOST': config('SUPABASE_HOST'),
            'USER': config('DB_USER'),
            'PASSWORD': config('SUPABASE_PASSWORD'),
            'PORT': config('PORT'),
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

if PRODUCTION and IS_REDIS:
    CACHE_TTL = 50 * 15
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": config("REDIS_LOCATION"),
            "OPTIONS": {
                "DB": 1,
                "PASSWORD": config("REDIS_PASSWORD"),
                'parser_class': config("PARSER_CLASS"),
                'pool_class': config('POOL_CLASS'),
                "CLIENT_CLASS": config('CLIENT_CLASS'),
            }
        }
    }
    SESSION_ENGINE = config("SESSION_ENGINE")
    SESSION_CACHE_ALIAS = config("SESSION_CACHE_ALIAS")
elif IS_MEMCACHED:
    CACHE_TTL = 3600
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
    SESSION_ENGINE = config("SESSION_ENGINE")
    SESSION_CACHE_ALIAS = config("SESSION_CACHE_ALIAS")
else:
    CACHE_TTL = 0 * 0
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'removePlugins': 'stylesheetparser',
        'toolbar': 'full',
        'height': 900,
        'width': 900,
    },
}


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework_api_key.permissions.HasAPIKey",
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )

}

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
    "rest_framework.renderers.JSONRenderer",
)
"""Simple JWT related settings"""

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS512',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=10),
    'AUTH_TOKEN_SAMESITE': 'None',
}
""" CORS origin settings"""

CORS_ALLOWED_METHODS = [
    'GET',
    'POST',
]


CORS_ORIGIN_ALLOW_ALL = False

PASSWORD_RESET_TIME_OUT = 900  # in seconds

# Logging setup
# HTTPS settings
if PRODUCTION:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    ##
    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
if PRODUCTION:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_SIGNATURE_NAME = 's3v4',
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    AWS_S3_VERITY = True
    AWS_QUERYSTRING_AUTH = False
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = "storages.backends.s3.S3Storage"
    S_MODE = "static"
    M_MODE = "media"
    STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}/'
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}/'
