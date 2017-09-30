"""
Django settings for asemi project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd5x%1@ee2un397s@=#a9k(s*mty*dh4yqi$k&lw6w=#6e6)51n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['35.188.24.68', 'localhost', '104.197.92.205', '*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main'
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

ROOT_URLCONF = 'asemi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR+'/templates'
        ],
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

WSGI_APPLICATION = 'asemi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'asemidb',
        'USER': 'asemi_user',
        # 'PASSWORD': 'zO2xwyHbEGlSSzZ5',
        'PASSWORD': 'asemi_user12345',
        'HOST': '35.188.75.186',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT= '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

'''Project Constants'''

FUNCTIONS = {
    'FRAC':r"([a-zA-Z]+ |\\frac|\{\d+}|\{[a-zA-Z]+}|\\sinh|\\sin|\\cosh|\\coth|\\cos|\\tanh|\\tan|\\csch|\\csc|\\sech|\\sec|\\cot|\\ln|\\log|\\infty|\\pi|\\mu|\\cap|\\cup|\\leq|\\geq|\\rightarrow|\\leftrightarrow|\\leftarrow|\\forall|\\exists|\\neg|\\nexists|\\sum|\\int|\\oint|\\sqrt|\\Vec|\\langle|\\rangle|\\uparrow|\\downarrow|\\arccos|\\arcsin|\\arctan|\\arcsec|\\arccsc|\\arccot|\\det|\\exp|\\liminf|\\limsup|\\lim|\\max|\\min|\\sup|\\alpha|\\beta|\\gamma|\\delta|\\epsilon|\\varepsilon|\\zeta|\\eta|\\theta|\\vartheta|\\iota|\\kappa|\\lambda|\\mu|\\nu|\\xi|\\pi|\\varpi|\\rho|\\varrho|\\sigma|\\varsigma|\\tau|\\upsilon|\\phi|\\varphi|\\chi|\\psi|\\omega|\\Gamma|\\Delta|\\Theta|\\Lambda|\\Xi|\\Pi|\\Sigma|\\Upsilon|\\Phi|\\Psi|\\Omega|\\pm|\\mp|\\times|\|\\div|\\star|\\circ|\\bullet|\\cdot|\\cap|\\cup|\\vee|\\wedge|\\diamond|\\leq|\\prec|\\bigtriangledown|\\bigtriangleup|\\subset|\\subseteq|\\in|\|\\supset|\\supseteq|\\equiv|\\approx|\\neq|\<|\\perp|\\parallel|\=|\>|\\sum|\\prod|\\int|\\oint|\\colon|\\leftarrow|\\nleftarrow|\\rightarrow|\\nrightarrow|\\leftrightarrow|\\nleftrightarrow|\\uparrow|\\downarrow|\\nearrow|\\searrow|\\Re|\\cdots|\\nabla|\\top|\\to|\\bot|\\vdots|\\forall|\\exists|\\exists!|\\neg|\\backslash|\\partial|\\infty|\\emptyset|\\nless|\\nparallel|\\measuredangle|\\mho|\\complement|\\angle|\\varnothing|\^)"
}

