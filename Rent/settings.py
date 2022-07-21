from environs import Env
import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import sys
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!:
DEBUG = os.getenv("DEBUG", "False") == "True"



ALLOWED_HOSTS = ['rent4less.com.ng', '127.0.0.1', "localhost"]


DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"
# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'House',
    'customer',
    'crispy_forms',
    'django_filters',
    'payment',
    'bootstrap3',
    'django_pandas',
    'basket',
    'user_visit',
    'mathfilters',
    'subscriptions',
    # 'django_crontab',
]


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Rent4Less Admin",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Rent4Less|Dashboard",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "R4L",

    "welcome_sign": "Welcome to Rent4Less",

    "site_logo": "asseting/img/rent4less-logo-small.png",

    # Copyright on the footer
    "copyright": "Designed by emmysoln",

    "changeform_format": "single",

    "icons": {
        "auth": "fas fa-users-user",
        "auth.user": "fas fa-user",
        "users.user_visits": "fas fa-user",
        "users.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        "House.Apartment": "fas fa-home",
        "House.Room": "fas fa-bed",
        "House.City": "fas fa-city",
        "customer.Userprofile": "fas fa-users",
        "customer.Contact": "far fa-address-book",
        "customer.RoomCart": "fas fa-book",
        "payment.BookItem": "fas fa-book",
        "customer.Order": "fab fa-buysellads",
        "customer.MailMessage": "fas fa-book",
        "customer.Subscribers": "far fa-address-book",
        "House.Testemonial": "fas fa-user",
        "Customer.Profile": "fas fa-user",
        "Customer.LandLord": "fas fa-user",
        "House.Estate": "fas fa-home",
        "House.AdminMessage": "fas fa-book",
        "House.EstateHistory": "fas fa-history",
        "House.EstateImage": "fas fa-image",
        "payment.Payment": "fas fa-credit-card",
        "payment.Payment_list": "fas fa-address-card",
    },

    "topmenu_links": [
        {"name": "Dashboard", "url": "dashboard"},
        {"name": "Home", "url": "home"},
    ],

}


CRISPY_TEMPLATES_PACKS = 'bootstrap4'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'user_visit.middleware.UserVisitMiddleware'
]

ROOT_URLCONF = 'Rent.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'basket.context_processors.basket',
            ],
        },
    },
]

WSGI_APPLICATION = 'Rent.wsgi.application'


if DEVELOPMENT_MODE is True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if os.getenv("DATABASE_URL", None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
    }


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

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# media file for serving images
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# AUTH_USER_MODEL = 'Users.CustomUser'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",


    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },

    "navbar": "navbar-dark",
    "no_navbar_border": False,
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587


PAYSTACK_SECRET_KEY = env.str('PAYSTACK_SECRET_KEY')
PAYSTACK_PUBLIC_KEY = env.str('PAYSTACK_PUBLIC_KEY')


BASKET_SESSION_ID = 'basket'

  