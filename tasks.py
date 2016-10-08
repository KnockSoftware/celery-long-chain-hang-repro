import os
import random
import logging

logger = logging.getLogger(__name__)

from celery import Celery

redis_hostname = os.getenv('REDIS_HOSTNAME')
app = Celery('hello', broker='redis://{}/0'.format(redis_hostname))
app.add_defaults(dict(
    CELERY_RESULT_BACKEND='redis://{}/1'.format(redis_hostname),
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json'
))

@app.task(bind=True)
def simple(self, something=None):
    logger.warning('SIMPLE simple {}'.format(something))
    return 'simple return'
