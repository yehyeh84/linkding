"""
Development settings for linkding webapp
"""

# Start from development settings
# noinspection PyUnresolvedReferences
from .base import *

# Turn on debug mode
DEBUG = True
# Turn on SASS compilation
SASS_PROCESSOR_ENABLED = True

# Enable debug toolbar
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

INTERNAL_IPS = [
    '127.0.0.1',
]

# Allow access through ngrok
CSRF_TRUSTED_ORIGINS = ['https://*.ngrok-free.app']

# Enable debug logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {module}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
                'class':'logging.handlers.RotatingFileHandler',
                'filename': './data/log.txt',
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
                'formatter':'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',  # Set to DEBUG to log all SQL calls
            'handlers': ['console'],
        },
        'bookmarks': {  # Log importer debug output
            'level': 'DEBUG',
            'handlers': ['console','file'],
            'propagate': False,
        }
    }
}

# Import custom settings
# noinspection PyUnresolvedReferences
from .custom import *
