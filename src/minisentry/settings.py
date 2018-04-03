import os

from dotenv import load_dotenv

from django.contrib import admin

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_path = os.path.expanduser(os.environ.get("MINISENTRY_ENV_PATH", "~/.minisentry.env"))
if os.path.isfile(dotenv_path):
    load_dotenv(dotenv_path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '29z71y^5lks9!qy-nnlycry0wze*@9uv(3o37awo^2ar#il6=q')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = list(
    map(lambda x: x.strip(), os.environ.get("ALLOWED_HOSTS", "localhost").split(","))
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'minisentry',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'minisentry.urls'

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

WSGI_APPLICATION = 'minisentry.wsgi.application'


# Database
db_settings = {
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.expanduser(os.environ.get("DB_NAME", "~/minisentry.sqlite3")),
    },
    "postgresql": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
    },
    "mysql": {
        "ENGINE": "django.db.backends.mysql",
    }
}
db_common = {
    "NAME": os.environ.get("DB_NAME", "minisentry"),
    "USER": os.environ.get("DB_USER", ""),
    "PASSWORD": os.environ.get("DB_PASSWORD", ""),
    "HOST": os.environ.get("DB_HOST", ""),
    "PORT": os.environ.get("DB_PORT", ""),
}
db_settings["postgresql"].update(db_common)
db_settings["mysql"].update(db_common)

DB_ENGINE = os.environ.get("DB_ENGINE", "sqlite")
DATABASES = {
    "default": db_settings[DB_ENGINE],
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
STATIC_DIR_MINISENTRY = os.path.join(os.path.dirname(__file__), "static", "minisentry")
STATIC_DIR_ADMIN = os.path.join(os.path.dirname(admin.__file__), "static", "admin")


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {
            "format": "%(levelname)s %(asctime)s %(name)s %(message)s",
            'datefmt': "%d.%m.%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": os.environ.get("LOGGING_CONSOLE_FORMATTER", "simple")
        }
    },
    "loggers": {
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

if DEBUG:
    LOGGING["formatters"]["colored"] = {
        "()": "colorlog.ColoredFormatter",
        "format":
            "%(log_color)s%(levelname)-8s%(reset)s %(blue)s[%(asctime)s %(name)s:%(lineno)s] "
            "%(white)s%(message)s",
        "datefmt": "%H:%M:%S",
    }


LOGIN_URL = "/signin/"
LOGIN_REDIRECT_URL = "/sentry/"

USE_SILK = os.environ.get("USE_SILK", "False") == "True"
if DEBUG and USE_SILK:
    INSTALLED_APPS += ["silk", ]
    MIDDLEWARE += ["silk.middleware.SilkyMiddleware", ]


# Email settings
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "anti1869@gmail.com")
DEFAULT_FROM_EMAIL_FULL = f"MiniSentry <{DEFAULT_FROM_EMAIL}>"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = os.environ.get("EMAIL_PORT", "25")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False") == "True"

# Web server options
MINISENTRY_WEB_HOST = os.environ.get("MINISENTRY_WEB_HOST", "0.0.0.0")
MINISENTRY_WEB_PORT = os.environ.get("MINISENTRY_WEB_PORT", 9000)
MINISENTRY_WEB_STATS_ENABLE = os.environ.get("MINISENTRY_WEB_STATS_ENABLE", "True") == "True"
MINISENTRY_WEB_STATS_HOST = os.environ.get("MINISENTRY_WEB_STATS_HOST", "127.0.0.1")
MINISENTRY_WEB_STATS_PORT = os.environ.get("MINISENTRY_WEB_STATS_PORT", 9191)
MINISENTRY_WEB_SERVE_STATIC = os.environ.get("MINISENTRY_WEB_SERVE_STATIC", "True") == "True"
MINISENTRY_WEB_MULE_COUNT = int(os.environ.get("MINISENTRY_WEB_MULE_COUNT", 2))

# Misc
MULE_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "mule.py")
MINISENTRY_URL_PREFIX = os.environ.get("MINISENTRY_URL_PREFIX", "http://localhost:8000")
MINISENTRY_URL_SCHEMA, MINISENTRY_URL_HOST = MINISENTRY_URL_PREFIX.split("://")
KEEP_DATA_FOR_DAYS = int(os.environ.get("KEEP_DATA_FOR_DAYS", 90))
