import os
from pathlib import Path

import dynaconf  # noqa

SECRET_KEY = (
    "django-insecure-b7d*13+ri7&-^h+7g^*!t#_nctn%47147+s2-l6l^hf)ki=i5l"
)

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = []  # type: ignore

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "crispy_forms",
    "django_htmx",
    "django_extensions",
    "rosetta",
    "apps.user",
    "apps.base",
    "apps.center",
    "apps.person",
    "apps.workgroup",
    "apps.event",
    "apps.treasury",
    "apps.publicwork",
    "apps.presidium",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

# removing debug_toobar in production
if DEBUG is False:
    del INSTALLED_APPS[6]
    del MIDDLEWARE[0]

ROOT_URLCONF = "rcadmin.urls"

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
                "django.contrib.messages.context_processors.messages",
                "rcadmin.context_processors.export_vars",
            ],
        },
    },
]
TEMPLATE_CONTEXT_PROCESSORS = "Django.core.context_processors.i18n"
CRISPY_TEMPLATE_PACK = "bootstrap4"

WSGI_APPLICATION = "rcadmin.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]
AUTH_USER_MODEL = "user.User"

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("pt-br", "Portuguese"),
]
LOCALE_PATHS = [
    BASE_DIR / "locale",
]

LOAD_DOTENV = True
LOGIN_REDIRECT_URL = "/user/profile/detail/"
LOGIN_URL = "login"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
APP_NAME = "rc@admin"

DEFAULT_SETTINGS_PATHS = ["settings.yaml", ".secrets.yaml"]

INTERNAL_IPS = ["127.0.0.1"]  # comment this line to disallow debug_toolbar

# Dynaconf
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

settings = dynaconf.DjangoDynaconf(
    __name__,
    SETTINGS_FILE_FOR_DYNACONF="../settings.yaml",
    SECRETS_FOR_DYNACONF="../.secrets.yaml",
)  # noqa
