import os


def get_config(log_dir):
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format':
                "[%(asctime)s] %(levelname)s [%(name)s: %(funcName)s: %(lineno)s] %(message)s",
                'datefmt': "%Y-%m-%dT%H:%M:%S%z"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
            'django_log_file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir, 'django.log'),
                'maxBytes': 16777216,  # 16megabytes
                'formatter': 'verbose'
            },
            'apps_log_file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(log_dir, 'apps.log'),
                'maxBytes': 16777216,  # 16megabytes
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['django_log_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'django.request': {
                'handlers': ['django_log_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
            '': {
                'handlers': ['console', 'apps_log_file'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
    }
