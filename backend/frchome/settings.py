'''
Django settings for frchome project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
'''

from pathlib import Path
import environ
import datetime
import ldap
import os
from django_auth_ldap.config import LDAPSearch, GroupOfUniqueNamesType

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG = (bool, False),
    LDAP_TLS_REQUIRED = (bool, False)
)
env.prefix = 'DJANGO_'
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'simple_history',
    'drf_spectacular',
    # custom
    'api',
    'rules',
    'rulesetrequests',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

# Baseline configuration.
AUTH_LDAP_SERVER_URI = env('AUTH_LDAP_SERVER_URI')

if env('LDAP_TLS_REQUIRED'):
    LDAP_CA_FILE_PATH = env('LDAP_CA_FILE_PATH')
    AUTH_LDAP_CONNECTION_OPTIONS = {
        ldap.OPT_X_TLS_CACERTFILE: LDAP_CA_FILE_PATH,
        ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_ALLOW,
        ldap.OPT_X_TLS_NEWCTX: 0
    }

AUTH_LDAP_BIND_DN = env('AUTH_LDAP_BIND_DN')
AUTH_LDAP_BIND_PASSWORD = env('AUTH_LDAP_BIND_PASSWORD')

# Set up the basic user parameters.
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    base_dn=env('LDAP_USER_BASE_DN'),
    # cant load scope from env
    scope=ldap.SCOPE_SUBTREE,
    filterstr=env('LDAP_USER_FILTER')
)


# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    base_dn=env('LDAP_GROUP_BASE_DN'),
    # cant load scope from env
    scope=ldap.SCOPE_SUBTREE,
    filterstr=env('LDAP_GROUP_FILTER')
)

# cant load group type from env
AUTH_LDAP_GROUP_TYPE = GroupOfUniqueNamesType(name_attr='cn')

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    'first_name': 'givenName',
    'last_name': 'sn',
    'email': 'mail',
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = env.json('AUTH_LDAP_USER_FLAGS_BY_GROUP')

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# If True, LDAPBackend will be able furnish permissions for any Django user, regardless of which backend authenticated it.
AUTH_LDAP_AUTHORIZE_ALL_USERS = True

# Cache distinguished names and group memberships for an hour to minimize
# LDAP traffic.
AUTH_LDAP_CACHE_TIMEOUT = 3600

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'frchome.urls'

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

WSGI_APPLICATION = 'frchome.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': env.db(),
}

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


LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'handlers': {'console': {'class': 'logging.StreamHandler'}},
   'loggers': {'django_auth_ldap': {'level': env('LDAP_LOGGING_LEVEL'), 'handlers': ['console']}},
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = env('LANGUAGE_CODE')

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'api.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
#    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#    'PAGE_SIZE': 10
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ['Bearer'],
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(seconds=30),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(minutes=1),
}
