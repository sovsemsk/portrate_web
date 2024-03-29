import json
import os
from pathlib import Path

from django.urls import reverse_lazy
from dotenv import load_dotenv

load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

INSTALLED_APPS = [

    # Пакеты
    "admin_interface",
    "colorfield",
    "django_browser_reload",
    "django_celery_results",
    "django_filters",
    "debug_toolbar",
    "chartjs",

    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Приложения
    "extensions.apps.ExtensionsConfig",
    "resources.apps.ResourcesConfig",
    "feedback.apps.FeedbackConfig",
    "widget.apps.WidgetConfig",
    "dashboard.apps.DashboardConfig",
]

MIDDLEWARE = [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages"
            ]
        }
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": str(os.getenv("DATABASE_NAME")),
        "USER": str(os.getenv("DATABASE_USER")),
        "HOST": str(os.getenv("DATABASE_HOST")),
        "PASSWORD": str(os.getenv("DATABASE_PASSWORD")),
        "PORT": "5432"
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

# Env
DEBUG = json.loads(str(os.getenv("DEBUG")).lower())

# Addresses
HOST = str(os.getenv("HOST"))
ALLOWED_HOSTS = ["127.0.0.1", "geo.portrate.io"]
INTERNAL_IPS = ["127.0.0.1"]

# Auth paths
LOGIN_URL = reverse_lazy("user_login")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "$1_5!x!*_-vc&d7$usb94$pm)2h=q0+q))5wm96&#78l8#mn0"
ROOT_URLCONF = "po_web.urls"
WSGI_APPLICATION = "po_web.wsgi.application"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = "ru-ru"
LANGUAGES = [["ru", "Русский"]]
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = "static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# Telegram
TELEGRAM_BOT_API_SECRET = str(os.getenv("TELEGRAM_BOT_API_SECRET"))

#
SELENIUM_BOT_API_SECRET = str(os.getenv("SELENIUM_BOT_API_SECRET"))

# Celery
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 36000
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Django resized
DJANGORESIZED_DEFAULT_SIZE = [500, 500]
DJANGORESIZED_DEFAULT_SCALE = 1
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True