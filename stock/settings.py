from pathlib import Path
import os
from django.contrib import messages
from django.conf import settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-w)og3q2h**+dk4+t$lsqv@b7#n&qzjsgr(^qc#s&b+mojdv%h%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'app.CustomUser'

# Application definition
INSTALLED_APPS = [
    'admincharts',
    'jazzmin',
    'channels',
    'app',
    'api',
    'home',
    'settings',
    'blog',
    'mathfilters',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}




ASGI_APPLICATION = 'stock.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stock.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'app.context_processors.custom_admin_context',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'stock.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTHENTICATION_BACKENDS = [
    'app.backends.UsernameOrEmailBackend',  # Add the custom backend
    'django.contrib.auth.backends.ModelBackend',      # Default backend
]


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATICFILES_DIRS =[
#     os.path.join(BASE_DIR, "static"),
# ]


STATIC_URL = '/static/'
STATIC_ROOT = 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings
# CSRF_TRUSTED_ORIGINS = ['https://onstock.in']

# Login URL
LOGIN_URL = '/login/'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'onstocktrader@gmail.com'
EMAIL_HOST_PASSWORD = 'nurd mkis qbje aqsa'
EMAIL_USE_TLS = True

# Custom settings for Login Session

SESSION_COOKIE_AGE = 24 * 60 * 60  # 24 hours in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


PAYU_ENVIRONMENT = 'TEST'  # Use 'Production' in live


# File paths
SYMBOLS_FILE = 'C:\\Users\\atulg\\Desktop\\stock\\data\\symbols.csv'
DATA_FILE = 'C:\\Users\\atulg\\Desktop\\stock\\data\\data.csv'
LIMIT_ORDERS_FILE = 'C:\\Users\\atulg\\Desktop\\stock\\data\\limit_orders.csv'

JAZZMIN_SETTINGS = {
    "site_logo": 'images/brand/logo/brand.png',
    "login_logo": 'images/brand/logo/brand.png',
    "site_logo_classes":'img-circle',
}

ADMIN_CHARTS_NVD3_JS_PATH = 'bow/nvd3/build/nv.d3.js'
ADMIN_CHARTS_NVD3_CSS_PATH = 'bow/nvd3/build/nv.d3.css'
ADMIN_CHARTS_D3_JS_PATH = 'bow/d3/d3.js'