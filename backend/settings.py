"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _
from .custom.functions import summernote_upload_to
from import_export.formats.base_formats import CSV, XLSX


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5c8x=ye%royvhmuq-k72ztb_a^at7h-!w!g%6v*x$db&tx^lo)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == 'True'

ALLOWED_HOSTS = ['*']

INTERNAL_IPS = [
    "127.0.0.1",
]

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'rosetta',
    'parler',
    'django_summernote',
    'debug_toolbar',
    'import_export',
    'daphne',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app_gateway',
    'app_account',
    'app_article',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'backend.custom.middleware.AcceptRangesMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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

WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = 'backend.asgi.application'


# Channel

CHANNEL_LAYERS = {
    "default": {
        # "BACKEND": "channels_redis.core.RedisChannelLayer",
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        # "CONFIG": {
        #     "hosts": [("127.0.0.1", 6379)],
        # },
    },
}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("DB_NAME"),
#         "USER": os.getenv("DB_USER"),
#         "PASSWORD": os.getenv("DB_PASSWORD"),
#         "HOST": os.getenv("DB_HOST"),
#         "PORT": os.getenv("DB_PORT"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Rest framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


# Allow cors-header

X_FRAME_OPTIONS = 'ALLOWALL'
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ORIGIN_ALLOW_ALL = True
XS_SHARING_ALLOWED_METHODS = ['GET']


#  Swagger

SWAGGER_SETTINGS = {
    # 'SUPPORTED_SUBMIT_METHODS': ['*'],  # Due to bug described above
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
    },
    # 'DEFAULT_AUTO_SCHEMA_CLASS': 'backend.custom.schema.CustomAutoSchema',
    'LOGIN_URL': '/admin/login/',
    'LOGOUT_URL': '/admin/logout/'
}


# Jazzmin

JAZZMIN_UI_TWEAKS = {
    "theme": "default",
    "dark_mode_theme": "darkly",
}

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": _("Django core Admin"),

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": _("Django core"),

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": _("Django core"),

    # Logo to use for your site, must be present in static files, used for brand on top left
    # "site_logo": "favicon.ico",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": None,

    # Copyright on the footer
    "copyright": "",

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": _("Trang chủ"),  "url": "admin:index", "permissions": ["auth.view_user"]},
    ],

    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,

    'hide_apps': ["django_summernote"],

    "hide_models": [],

    "order_with_respect_to": ["auth", "app_account", "admin.LogEntry"],

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth.Group": "fas fa-users",
        "auth.User": "fas fa-user",
        "admin.LogEntry": "fas fa-history",
        "app_article.Article": "fas fa-newspaper",
        "app_account.APIKey": "fas fa-key",
        "app_account.User": "fas fa-user",
    },
    # Icons that are used when one is not manually specified
    # "default_icon_parents": "fas fa-chevron-circle-right",
    # "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,

    #############
    # UI Tweaks #
    #############
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    "changeform_format": "horizontal_tabs",
    # # Add a language dropdown into the admin
    "language_chooser": True,
}


# Logging

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'action_file': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(BASE_DIR, 'logs/action_log.log'),
#             'maxBytes': 1024 * 1024 * 10,
#             'backupCount': 3,
#             'formatter': 'verbose',
#             'encoding':'utf8',
#         },
#         'error_file': {
#             'level': 'ERROR',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(BASE_DIR, 'logs/error_log.log'),
#             'maxBytes': 1024 * 1024 * 10,
#             'backupCount': 3,
#             'formatter': 'verbose',
#             'encoding':'utf8',
#         },
#     },
#     'loggers': {
#         'django.db.models': {
#             'handlers': ['action_file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#         'django': {
#             'handlers': ['error_file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'vi'

LANGUAGES = (
    ('vi', _('Tiếng Việt')),
    ('en', _('English')),
    ('zh-hans', _('中国'))
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True


# Parler language

PARLER_DEFAULT_LANGUAGE_CODE = 'vi'

PARLER_LANGUAGES = {
    None: (
        {'code': 'vi',},
        {'code': 'en',},
        {'code': 'zh-hans',}
    ),
    'default': {
        'fallbacks': ['vi'],
        'hide_untranslated': False,
    }
}


# Django-resized

DJANGORESIZED_DEFAULT_SIZE = [1920, 1080]
DJANGORESIZED_DEFAULT_SCALE = 1.0
DJANGORESIZED_DEFAULT_QUALITY = 100
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'webp'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'webp': ".webp"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True


# Summernote

SUMMERNOTE_CONFIG = {
    'attachment_require_authentication': True,
    'disable_attachment': False,
    'attachment_absolute_uri': False,
    'attachment_upload_to': summernote_upload_to(),
    'attachment_filesize_limit': 102400000
}


# Debug toolbar

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: os.getenv("SHOW_DEBUG_TOOLBAR") == 'True'
}


# Django-import-export

IMPORT_EXPORT_FORMATS = [CSV, XLSX]
IMPORT_EXPORT_IMPORT_PERMISSION_CODE = 'change'
IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'change'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'staticfiles']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

API_URL = os.getenv("API_URL")


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'app_account.User'