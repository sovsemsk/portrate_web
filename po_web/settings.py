import json
import os
from pathlib import Path

from django.urls import reverse_lazy
from dotenv import load_dotenv

load_dotenv()

"""
LOGGING = {
    "version": 1,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["console"],
        }
    }
}
"""

# Django
ADMINS = [["Eugene", "sovsemsk@gmail.com"]]
ALLOWED_HOSTS = ["127.0.0.1", "geo.portrate.io"]
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"}
]
BASE_DIR = Path(__file__).resolve().parent.parent
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}
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
DEBUG = json.loads(str(os.getenv("DEBUG")).lower())
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
INSTALLED_APPS = [

    # Пакеты
    "admin_interface",
    "colorfield",
    "django_celery_beat",
    "django_celery_results",
    "django_filters",

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
    "dashboard.apps.DashboardConfig"
]
LANGUAGE_CODE = "ru-ru"
LANGUAGES = [["ru", "Русский"]]
LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]
LOGIN_URL = reverse_lazy("user_login")
LOGIN_REDIRECT_URL = reverse_lazy("company_list")
LOGOUT_REDIRECT_URL = reverse_lazy("company_list")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware"
]
ROOT_URLCONF = "po_web.urls"
SECRET_KEY = "$1_5!x!*_-vc&d7$usb94$pm)2h=q0+q))5wm96&#78l8#mn0"
SESSION_COOKIE_AGE = 86400
SILENCED_SYSTEM_CHECKS = ["security.W019"]
STATIC_ROOT = "static/"
STATIC_URL = "static/"
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
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
WSGI_APPLICATION = "po_web.wsgi.application"
X_FRAME_OPTIONS = "SAMEORIGIN"

# Celery
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_CACHE_BACKEND = "default"
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 86400
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Django resized
DJANGORESIZED_DEFAULT_SIZE = [500, 500]
DJANGORESIZED_DEFAULT_SCALE = 1
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = "JPEG"
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {"JPEG": ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

# Selenium
SELENIUM_BOT_API_SECRET = str(os.getenv("SELENIUM_BOT_API_SECRET"))

# Telegram
TELEGRAM_BOT_API_SECRET = str(os.getenv("TELEGRAM_BOT_API_SECRET"))
