#import os
from environ import Env, Path

ENV = Env()
Env.read_env()
SECRET_KEY = ENV("SECRET_KEY")
BASE_DIR = Path(__file__) - 3


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = '^y*ypqc(^f0fpo^9*s9=i2*i-_jr*pn(g&xet@w=jf_&%^)!o@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # third party
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'oauth2_provider',
    'corsheaders',
    #"url_checks.apps.UrlChecksConfig",
    # first party
    'blog.apps.BlogConfig',
    'organizer.apps.OrganizerConfig',
    'user.apps.UserConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'drf_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR("templates")],
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

WSGI_APPLICATION = 'drf_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'testdriven',
        'USER': 'lmarinve',
        'PASSWORD': 'fussy',
        'HOST': 'localhost',
        'PORT': '',
    }
}

def get_memcache_config():
    """Load config from ENV, or assume Heroku deploy

    https://devcenter.heroku.com/articles/memcachier#django
    """
    if ENV.get_value("MEMCACHE_URL", default=None):
        return ENV.cache("MEMCACHE_URL")
    location = ENV.get_value(
        "MEMCACHIER_SERVERS", default=None
    )
    if location:
        return {
            "BACKEND": "django.core.cache.backends.memcached.PyLibMCCache",
            "TIMEOUT": None,  # default key expiration, NOT connection timeout
            "LOCATION": ENV.str("MEMCACHIER_SERVERS"),
            "OPTIONS": {
                "binary": True,
                "username": ENV.str("MEMCACHIER_USERNAME"),
                "password": ENV.str("MEMCACHIER_PASSWORD"),
                "behaviors": {
                    # Enable faster IO
                    "no_block": True,
                    "tcp_nodelay": True,
                    # Keep connection alive
                    "tcp_keepalive": True,
                    # Timeout settings
                    "connect_timeout": 2000,  # ms
                    "send_timeout": 750 * 1000,  # us
                    "receive_timeout": 750 * 1000,  # us
                    "_poll_timeout": 2000,  # ms
                    # Better failover
                    "ketama": True,
                    "remove_failed": 1,
                    "retry_timeout": 2,
                    "dead_timeout": 30,
                },
            },
        }
    return {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache"
    }


CACHE_MIDDLEWARE_KEY_PREFIX = "startuporganizer"
CACHE_MIDDLEWARE_SECONDS = 60

CACHES = {"default": get_memcache_config()}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL='user.User'

ACCOUNT_ACTIVATION_DAYS = ENV(
    "ACCOUNT_ACTIVATION_DAYS", default=7
)
# https://django-registration.readthedocs.io/en/3.0.1/activation-workflow.html#salt-security
REGISTRATION_SALT = ENV(
    "REGISTRATION_SALT", default="registration"
)


PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]

AUTH_P = "django.contrib.auth.password_validation."
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": AUTH_P + "UserAttributeSimilarityValidator",
        "OPTIONS": {
            "user_attributes": ("email", "full_name", "short_name" )
        },
    },
    {
        "NAME": AUTH_P + "MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": AUTH_P + "CommonPasswordValidator"},
    {"NAME": AUTH_P + "NumericPasswordValidator"},
]

LOGIN_URL = "auth:login"
LOGIN_REDIRECT_URL = "site_root"
LOGOUT_REDIRECT_URL = "auth:login"

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 1,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.IsAuthenticatedOrTokenHasScope",
        "rest_framework.permissions.DjangoModelPermissions",
    ),
}

OAUTH2_PROVIDER = {
    "SCOPES": {
        "newslink": "Access to news article links",
        "post": "Access to blog posts",
        "startup": "Access to startup data",
        "tag": "Access to tag (labels) data",
    }
}


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = BASE_DIR("runtime", "static")
STATIC_URL = "/static/"
STATICFILES_STORAGE = (
    "django.contrib.staticfiles.storage.StaticFilesStorage"
)

STATICFILES_DIRS = [BASE_DIR("static_content")]
WHITENOISE_ROOT = BASE_DIR("static_root")
