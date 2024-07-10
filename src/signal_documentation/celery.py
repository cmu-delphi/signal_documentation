from __future__ import absolute_import, unicode_literals

import os

from celery import Celery, Task
from celery.schedules import crontab
from django.conf import settings
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'signal_documentation.settings')

app = Celery('signal_documentation')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS, related_name='tasks')
app.conf.broker_connection_retry_on_startup = True

app.conf.beat_schedule = {}


class BaseTaskWithRetry(Task):
    """
    A base class for Celery tasks with automatic retry behavior.

    This class serves as a base for Celery tasks that require automatic retrying
    in case of exceptions. It provides default settings for retry behavior.

    Attributes:
        autoretry_for (tuple): A tuple of exception classes for which the task
            should be retried automatically.
        max_retries (int): The maximum number of times the task should be retried.
        default_retry_delay (int): The default delay (in seconds) before retrying
            the task after an exception.
        retry_backoff (bool): Indicates whether to use exponential backoff for
            retry delays or use the default_retry_delay.
        retry_backoff_max (int): The maximum delay (in milliseconds) to be used
            in the exponential backoff calculation.
        retry_jitter (bool): Indicates whether to introduce jitter in the retry
            delays to prevent tasks from retrying at the exact same time.

    """
    autoretry_for = (Exception,)
    max_retries = 3
    default_retry_delay = 3
    retry_backoff = False
    retry_backoff_max = 700
    retry_jitter = False


app.conf.beat_schedule = {
    'get_covidcast_meta': {
        'task': 'signals.tasks.get_covidcast_meta',
        'schedule': crontab(minute=1, hour=0),
    },
}
