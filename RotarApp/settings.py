import os
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECRET_KEY = os.getenv('KEY')
SECRET_KEY = "h5l%fev*eb22%3!2wf0e^&57-c^ke5c__5ea8kj-phdabqs)4p"

DEBUG = False

ALLOWED_HOSTS = ['www.rotaractdistrict3131.org']

if(settings.DEBUG) :
    ALLOWED_HOSTS += ['localhost','127.0.0.1']

INSTALLED_APPS = [
    'Auth.apps.AuthConfig',
    'SecReport.apps.SecreportConfig',
    'DistReport.apps.DistreportConfig',
    'Main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_sass',
    'crispy_forms',
    'xlrd'
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

ROOT_URLCONF = 'RotarApp.urls'

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
                'Main.context_processor.navbar_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'RotarApp.wsgi.application'

if not (settings.DEBUG) :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ss0506$prasad',
            'USER': 'ss0506',
            'PASSWORD':'babubhaiya',
            'HOST': 'ss0506.mysql.pythonanywhere-services.com',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            }
        }
    }

else :
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'rotarapp_reboot',
            'USER': 'root',
            'HOST': 'localhost',
            'PORT': '3306',
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            }
        }
}

AUTH_USER_MODEL = 'Auth.Account'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL = 'main_home'
LOGOUT_REDIRECT_URL = 'auth_login'
SIGNUP_REDIRECT_URL = 'main_home'
LOGIN_URL = '/login'

# Production Checklist
CRISPY_TEMPLATE_PACK = 'bootstrap4'

if not (settings.DEBUG) :
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 300
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'rotaract3131web@gmail.com'
    EMAIL_HOST_PASSWORD = 'babubhaiya'