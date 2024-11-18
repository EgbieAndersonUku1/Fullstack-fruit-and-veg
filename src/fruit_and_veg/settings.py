"""
Django settings for src project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from os.path import join
from dotenv import load_dotenv
from os import getenv
import logging

# Enables the `.env` file to be loaded
# load_dotenv()
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = join(BASE_DIR, "templates")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv("DEBUG")


# set the path for the custom user model
AUTH_USER_MODEL = "authentication.User"




# Fetch the ALLOWED_HOSTS environment variable, defaulting to an empty string if not set
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    ".vercel.app",
    ".now.sh",
]



# Application definition

INSTALLED_APPS = [
    'jazzmin',     
    'django_select2',
    'django_ckeditor_5',
  
     
    # my apps
    "home.apps.HomeConfig",
    "account.apps.AccountConfig",
    
    "authentication.apps.AuthenticationConfig",
    "blog.apps.BlogConfig",
    "user_profile.apps.UserProfileConfig",
    "subscription.apps.SubscriptionConfig",
    "testimonal.apps.TestimonalConfig",
                       
    # third party django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'fruit_and_veg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'authentication.context_processor.render_authentication_forms',
                'testimonal.context_processor.get_approved_testimonials',
                'subscription.context_processor.get_subscription_session',
            ],
        },
    },
]

WSGI_APPLICATION = 'fruit_and_veg.wsgi.application'


JAZZMIN_SETTINGS = { 
        
        "site_brand": "EUOrganics",
        "welcome_sign": "Welcome to the EUOrganics",
        "copyright": "EUOrganics Ltd",
      
                
}


# Gmail 
EMAIL_BACKEND       = getenv('EMAIL_BACKEND')
EMAIL_HOST          = getenv('EMAIL_HOST')
EMAIL_PORT          = getenv('EMAIL_PORT')
EMAIL_USE_TLS       = getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER     = getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases



# Determine database configuration based on the USE_LOCAL_DB environment variable
# If USE_LOCAL_DB is set to True, use local database settings
# Otherwise, use the production database settings

#USE_LOCAL_DB = getenv("LOCAL_DB", "").strip().title() in ["True", "1"] 
#print( getenv("LOCAL_DB", ""))

USE_LOCAL_DB = True  # set this line manually to use local DB since .env files is not picking it up

if USE_LOCAL_DB:
    print("Using local postgres db")
    DB_NAME     = getenv("DB_LOCAL_NAME")
    DB_USER     = getenv("DB_LOCAL_USER")
    DB_PASSWORD = getenv("DB_LOCAL_PASSWORD")
    DB_HOST     = getenv("DB_LOCAL_HOST")
    DB_PORT     = getenv("DB_LOCAL_PORT", "5432")
else:
    print("Using external postgres db")
    DB_NAME     = getenv("DB_NAME")
    DB_USER     = getenv("DB_USER")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST     = getenv("DB_HOST")
    DB_PORT     = getenv("DB_PORT")
   
   
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTION': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = '/static/'

# This is required if you are running collectstatic
STATIC_ROOT = join(BASE_DIR, 'staticfiles_build', 'static')

STATICFILES_DIRS = [
    join(BASE_DIR,  'static'),
]


MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



# redirects to a given url if the user is not login in

LOGIN_URL = '/'


# Ckeditor for rich text
customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
    ]


CKEDITOR_5_UPLOAD_FILE_TYPES = ['jpeg', 'png']


CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': ['heading', '|', 'bold', 'italic', 'link',
                    'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'autosave': {
            'saveDelay': 5000,  # 5 seconds delay before saving
            'storeData': ['content'],
        },
        
        'toolbar': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
                     "|", 'undo', 'redo', "|", 
        'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',],
      
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}

# CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"  