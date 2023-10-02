from django.shortcuts import render
import logging
# Create your views here.
from django.utils import timezone
from .models import LogEntry  # Import your custom LogEntry model


class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        LogEntry.objects.create(
            timestamp=timezone.now(),
            level=record.levelname,
            message=self.format(record)
        )


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django_blog.log',  # Specify the file path where logs will be stored
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
