import json
import os

import requests
from rest_framework.status import is_client_error, is_server_error

from signal_documentation.celery import BaseTaskWithRetry, app
from signals.tools import SignalLastUpdatedParser

COVID_CAST_META_URL = os.environ.get('COVID_CAST_META_URL', 'https://api.delphi.cmu.edu/epidata/covidcast/meta')


@app.task(bind=BaseTaskWithRetry)
def get_covidcast_meta(self):
    response = requests.get(COVID_CAST_META_URL, timeout=5)
    if is_client_error(response.status_code) or is_server_error(response.status_code):
        return f'{COVID_CAST_META_URL}. Error: {response.status_code} - {response.content}'

    if response.status_code == 200:
        parser = SignalLastUpdatedParser(covidcast_meta_data=json.loads(response.content))
        parser.set_data()
        return 'Signals last updated fields successfully updated'

    return f'Not success, status {response.status_code}'
