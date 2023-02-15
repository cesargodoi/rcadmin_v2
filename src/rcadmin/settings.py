import os
import dynaconf  # noqa

from pathlib import Path

SECRET_KEY = (
    "django-insecure-b7d*13+ri7&-^h+7g^*!t#_nctn%47147+s2-l6l^hf)ki=i5l"
)

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
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
]

MIDDLEWARE = [
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
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTH_USER_MODEL = "user.User"

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("pt-br", "Portuguese"),
]
LOCALE_PATHS = [
    "home/base/dev/projects/rcadmin/rcadmin/locale",
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


# Dynaconf
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

settings = dynaconf.DjangoDynaconf(
    __name__,
    SETTINGS_FILE_FOR_DYNACONF="../settings.yaml",
    SECRETS_FOR_DYNACONF="../.secrets.yaml",
)  # noqa
