"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)

SECRET_KEY = env('SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'oauth',
    'GPT',
    'apis',
    'writings',

    'drf_yasg',
    'openai',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + 'db.sqlite3',
    }
}

############################################

# 여기부터 유저 모델 관련
AUTH_USER_MODEL = 'users.UserModel'
AUTHENTICATION_BACKENDS = (
    'users.lib.backends.SettingsBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# DRF 인증 설정
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [  # 기본 Permission 설정
        'rest_framework.permissions.AllowAny',  # 모든 계정 액세스 허용
        # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (  # Authenticationt 설정
        # 'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': [  # api 결과 전달 방식
        'rest_framework.renderers.JSONRenderer',  # json 방식
    ],
    'DEFAULT_PARSER_CLASSES': [  # 요청 받을 때 body 형태
        'rest_framework.parsers.JSONParser',
        # 'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',  # serializer datetime format
}

# 여기부터 로그인 관련
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_PASSWORD_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'


# JWT 설정
REST_USE_JWT = False
ACCOUNT_LOGOUT_ON_GET = False
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS512',
    'SIGNING_KEY': '',

    'AUTH_HEADER_TYPES': ('Bearer',),  # 인증 헤더 유형
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',  # 인증 헤더 명칭
    'USER_ID_FIELD': 'social_id',  # 사용자 식별을 위한 토큰에 포함할 사용자 모델의 DB 필드명
    'USER_ID_CLAIM': 'social_id',  # 사용자 식별을 저장하는 데 사용할 생성된 토큰의 클레임

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # 토큰 유형 지정 클래스
    'TOKEN_TYPE_CLAIM': 'token_type',  # 토큰 유형 저장 클레임 명칭

    'JTI_CLAIM': 'jti',
}


# 소셜 로그인 설정
KAKAO_REST_API_KEY=env('KAKAO_REST_API_KEY')
KAKAO_REDIRECT_URI=env('KAKAO_REDIRECT_URI')
KAKAO_CLIENT_SECRET_KEY=env('KAKAO_CLIENT_SECRET_KEY')
############################################


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'