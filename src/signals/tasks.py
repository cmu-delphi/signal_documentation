import json
import os

import requests

from signal_documentation.celery import BaseTaskWithRetry, app

COVID_CAST_META_URL = os.environ.get('COVID_CAST_META_URL', 'https://api.covidcast.cmu.edu/epidata/covidcast/meta')


@app.task(BaseTaskWithRetry)
def get_covidcast_meta():
    response = requests.get(COVID_CAST_META_URL, timeout=5)
    if response is None:
        return f'Not response, url {COVID_CAST_META_URL}'

    if response.status_code == 200:
        return json.loads(response.content)

    return f'Not success, status {response.status_code}'
