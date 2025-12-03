# # """
# # Django settings for allicom_travels project.
# # Production-ready defaults, safe for local demo.
# # """

# # import os
# # from pathlib import Path
# # from decouple import config, Csv

# # # Base directory
# # BASE_DIR = Path(__file__).resolve().parent.parent

# # # ──────────────── Security ────────────────
# # SECRET_KEY = config('DJANGO_SECRET_KEY', default='replace-this-in-production')
# # DEBUG = config('DJANGO_DEBUG', default='True') == 'True'
# # # ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='127.0.0.1,localhost', cast=Csv)
# # hosts = config('DJANGO_ALLOWED_HOSTS', default='127.0.0.1,localhost')
# # ALLOWED_HOSTS = hosts.split(',') if isinstance(hosts, str) else hosts


# # # ──────────────── Installed Apps ────────────────
# # INSTALLED_APPS = [
# #     # Django core
# #     'django.contrib.admin',          # Remove if you don't use Django Admin
# #     'django.contrib.auth',
# #     'django.contrib.contenttypes',
# #     'django.contrib.sessions',
# #     'django.contrib.messages',
# #     'django.contrib.staticfiles',

# #     # Third-party
# #     'rest_framework',
# #     'django_filters',
# #     'corsheaders',

# #     # Local apps
# #     'users',
# #     'services',
# #     'payments',
# #     'bookings.apps.BookingsConfig',
# # ]

# # # ──────────────── Middleware ────────────────
# # MIDDLEWARE = [
# #     'django.middleware.security.SecurityMiddleware',
# #     'whitenoise.middleware.WhiteNoiseMiddleware',
# #     'corsheaders.middleware.CorsMiddleware',
# #     'django.contrib.sessions.middleware.SessionMiddleware',
# #     'django.middleware.common.CommonMiddleware',
# #     'django.middleware.csrf.CsrfViewMiddleware',
# #     'django.contrib.auth.middleware.AuthenticationMiddleware',
# #     'django.contrib.messages.middleware.MessageMiddleware',
# #     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# # ]

# # ROOT_URLCONF = 'allicom_travels.urls'

# # TEMPLATES = [
# #     {
# #         'BACKEND': 'django.template.backends.django.DjangoTemplates',
# #         'DIRS': [BASE_DIR / 'templates'],
# #         'APP_DIRS': True,
# #         'OPTIONS': {
# #             'context_processors': [
# #                 'django.template.context_processors.request',
# #                 'django.contrib.auth.context_processors.auth',
# #                 'django.contrib.messages.context_processors.messages',
# #             ],
# #         },
# #     },
# # ]

# # WSGI_APPLICATION = 'allicom_travels.wsgi.application'

# # # ──────────────── Database ────────────────
# # DATABASES = {
# #     'default': {
# #         'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
# #         'NAME': config('DB_NAME', default='allicom_travels'),
# #         'USER': config('DB_USER', default='postgres'),
# #         'PASSWORD': config('DB_PASSWORD', default=''),
# #         'HOST': config('DB_HOST', default='localhost'),
# #         'PORT': config('DB_PORT', default='5432'),
# #         'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=60, cast=int),
# #     }
# # }

# # # ──────────────── Authentication ────────────────
# # AUTH_USER_MODEL = 'users.User'

# # AUTH_PASSWORD_VALIDATORS = [
# #     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
# #     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
# #     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
# #     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
# # ]

# # # ──────────────── Internationalization ────────────────
# # LANGUAGE_CODE = 'en-us'
# # TIME_ZONE = config('TIME_ZONE', default='UTC')
# # USE_I18N = True
# # USE_TZ = True

# # # ──────────────── Static & Media ────────────────
# # STATIC_URL = '/static/'
# # STATIC_ROOT = BASE_DIR / 'staticfiles'
# # MEDIA_URL = '/media/'
# # MEDIA_ROOT = BASE_DIR / 'media'

# # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# # # ──────────────── REST Framework ────────────────
# # REST_FRAMEWORK = {
# #     'DEFAULT_AUTHENTICATION_CLASSES': (
# #         'rest_framework_simplejwt.authentication.JWTAuthentication',
# #     ),

# #     'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
# #     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
# #     'PAGE_SIZE': config('DRF_PAGE_SIZE', default=12, cast=int),
# # }


# # # ──────────────── CORS / CSRF ────────────────
# # CORS_ALLOWED_ORIGINS = config(
# #     'CORS_ALLOWED_ORIGINS',
# #     default='http://127.0.0.1,http://localhost',
# #     cast=Csv()
# # )

# # CSRF_TRUSTED_ORIGINS = config(
# #     'CSRF_TRUSTED_ORIGINS',
# #     default='http://127.0.0.1,http://localhost',
# #     cast=Csv()
# # )

# # # Allow all origins automatically when debugging
# # if DEBUG:
# #     CORS_ALLOW_ALL_ORIGINS = True

# # # ──────────────── Email ────────────────
# # EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
# # EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
# # EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
# # EMAIL_USE_TLS = config('EMAIL_USE_TLS', default='True') == 'True'
# # EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# # EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
# # DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Allicom Travels <noreply@yourdomain.com>')

# # # ──────────────── Security Headers ────────────────
# # if not DEBUG:
# #     SECURE_SSL_REDIRECT = config('DJANGO_SECURE_SSL_REDIRECT', default='True') == 'True'
# #     SESSION_COOKIE_SECURE = True
# #     CSRF_COOKIE_SECURE = True
# #     SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
# #     SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default='True') == 'True'
# #     SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default='True') == 'True'
# #     SECURE_BROWSER_XSS_FILTER = True
# #     SECURE_CONTENT_TYPE_NOSNIFF = True
# # else:
# #     SECURE_SSL_REDIRECT = False
# #     SESSION_COOKIE_SECURE = False
# #     CSRF_COOKIE_SECURE = False

# # # ──────────────── Logging ────────────────
# # LOGGING = {
# #     'version': 1,
# #     'disable_existing_loggers': False,
# #     'handlers': {
# #         'file': {
# #             'level': 'WARNING',
# #             'class': 'logging.FileHandler',
# #             'filename': BASE_DIR / 'logs' / 'django_warnings.log',
# #         },
# #         'console': {'class': 'logging.StreamHandler'},
# #     },
# #     'loggers': {
# #         'django': {
# #             'handlers': ['file', 'console'],
# #             'level': 'WARNING',
# #             'propagate': True,
# #         },
# #     },
# # }

# # DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # LOGGING = {
# #     'version': 1,
# #     'disable_existing_loggers': False,
# #     'handlers': {
# #         'bookings_file': {
# #             'level': 'ERROR',
# #             'class': 'logging.FileHandler',
# #             'filename': 'logs/bookings_signals.log',
# #         },
# #         'console': {
# #             'class': 'logging.StreamHandler',
# #         },
# #     },
# #     'loggers': {
# #         'bookings': {
# #             'handlers': ['bookings_file', 'console'],
# #             'level': 'ERROR',
# #             'propagate': True,
# #         },
# #     },
# # }

# """
# Django settings for allicom_travels project.
# Production-ready defaults, safe for local demo.
# """
# # import os
# # from pathlib import Path
# # from decouple import Config, Csv, RepositoryEnv





# # BASE_DIR = Path(__file__).resolve().parent.parent

# # # Load .env manually from project root
# # env_path = os.path.join(BASE_DIR, '.env')
# # config = Config(RepositoryEnv(env_path))

# import os
# from pathlib import Path
# from dotenv import load_dotenv
# from decouple import Config, Csv, RepositoryEnv

# # ──────────────── Base Directory ────────────────
# BASE_DIR = Path(__file__).resolve().parent.parent

# # ──────────────── Load .env Early ────────────────
# env_path = os.path.join(BASE_DIR, '.env')
# if os.path.exists(env_path):
#     load_dotenv(env_path)
#     print(f"✅ Loaded .env file from: {env_path}")
# else:
#     print("⚠️ WARNING: .env file not found — defaults or empty values may be used.")

# # ──────────────── Initialize decouple Config ────────────────
# config = Config(RepositoryEnv(env_path))

# # ──────────────── Debug Flutterwave Key Load ────────────────
# flw_key = os.getenv("FLW_SECRET_KEY")
# if not flw_key:
#     print("⚠️ WARNING: Flutterwave secret key not loaded! Check your .env file.")
# else:
#     print(f"✅ Flutterwave key loaded (starts with): {flw_key[:10]}...")


# SECRET_KEY = config('DJANGO_SECRET_KEY', default='replace-this-in-production')
# DEBUG = config('DJANGO_DEBUG', default='True') == 'True'
# hosts = config('DJANGO_ALLOWED_HOSTS', default='127.0.0.1,localhost')
# ALLOWED_HOSTS = hosts.split(',') if isinstance(hosts, str) else hosts

# FLW_SECRET_KEY = config('FLW_SECRET_KEY', default='')
# BASE_URL = config('BASE_URL', default='http://127.0.0.1:8000')


# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'rest_framework',
#     'django_filters',
#     'corsheaders',
#     'users',
#     'services',
#     'payments.apps.PaymentsConfig',   # 🟢 ADDED — ensures signals load via AppConfig
#     'bookings.apps.BookingsConfig',
# ]

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'corsheaders.middleware.CorsMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'allicom_travels.urls'

# TEMPLATES = [{
#     'BACKEND': 'django.template.backends.django.DjangoTemplates',
#     'DIRS': [BASE_DIR / 'templates'],
#     'APP_DIRS': True,
#     'OPTIONS': {
#         'context_processors': [
#             'django.template.context_processors.request',
#             'django.contrib.auth.context_processors.auth',
#             'django.contrib.messages.context_processors.messages',
#         ],
#     },
# }]

# WSGI_APPLICATION = 'allicom_travels.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': config('DB_ENGINE', default='django.db.backends.postgresql'),
#         'NAME': config('DB_NAME', default='allicom_travels'),
#         'USER': config('DB_USER', default='postgres'),
#         'PASSWORD': config('DB_PASSWORD', default=''),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#         'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=60, cast=int),
#     }
# }

# AUTH_USER_MODEL = 'users.User'

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = config('TIME_ZONE', default='UTC')
# USE_I18N = True
# USE_TZ = True

# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': config('DRF_PAGE_SIZE', default=12, cast=int),
# }

# CORS_ALLOWED_ORIGINS = config(
#     'CORS_ALLOWED_ORIGINS',
#     default='http://127.0.0.1,http://localhost',
#     cast=Csv()
# )
# CSRF_TRUSTED_ORIGINS = config(
#     'CSRF_TRUSTED_ORIGINS',
#     default='http://127.0.0.1,http://localhost',
#     cast=Csv()
# )
# if DEBUG:
#     CORS_ALLOW_ALL_ORIGINS = True

# EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
# EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
# EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', default='True') == 'True'
# EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
# DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Allicom Travels <noreply@yourdomain.com>')

# if not DEBUG:
#     SECURE_SSL_REDIRECT = config('DJANGO_SECURE_SSL_REDIRECT', default='True') == 'True'
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
# else:
#     SECURE_SSL_REDIRECT = False
#     SESSION_COOKIE_SECURE = False
#     CSRF_COOKIE_SECURE = False

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # CHANGED: unified/updated LOGGING block so payments logs go to file at INFO level.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'bookings_file': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'logs' / 'bookings_signals.log',
#         },
#         'payments_file': {
#             # CHANGED from 'ERROR' -> 'INFO' so informative messages are persisted
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'logs' / 'payments_signals.log',
#         },
#         'console': {'class': 'logging.StreamHandler'},
#     },
#     'loggers': {
#         'bookings': {
#             'handlers': ['bookings_file', 'console'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'payments': {
#             'handlers': ['payments_file', 'console'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#         'django': {
#             'handlers': ['console'],
#             'level': 'WARNING',
#             'propagate': True,
#         }
#     },
# }

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (.env)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
DEBUG = True

ALLOWED_HOSTS = ["*"]  # change in production

# APPLICATIONS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "corsheaders",

    # Local apps
    "users",
    "services",
    "bookings",
    "payments",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be at top
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "allicom_travels.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "allicom_travels.wsgi.application"

# DATABASE (PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "allicom_travels"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# PASSWORDS
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

# STATIC & MEDIA
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# CUSTOM USER MODEL
AUTH_USER_MODEL = "users.User"

# DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",  # users can book without logging in
    ],
}

# CORS
CORS_ALLOW_ALL_ORIGINS = True

# FLUTTERWAVE SETTINGS
FLW_SECRET_KEY = os.environ.get("FLW_SECRET_KEY")
FLW_PUBLIC_KEY = os.environ.get("FLW_PUBLIC_KEY")
FLW_REDIRECT_URL = os.environ.get("FLW_REDIRECT_URL")

# DEFAULT PK FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# from claude
# At the end of your settings.py file, add:

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
