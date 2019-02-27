from flask import Flask, request
import requests
from os import environ
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

auth_headers = {
        'X-Application-Id': environ.get('APP_ID', 'test'),
        'X-Api-Key': environ.get('APP_KEY', 'test'),
        'Accept': 'application/json',
        'Content-type': 'application/json'
    }


def proxy_to_source(url):
    url = f'https://api.traveltimeapp.com/{url}'
    return url


@app.route('/')
def root():
    return '.'


@app.route('/metrics',  methods=['GET', 'POST'])
def metrics():
    return 'Alive'


@app.route('/TravelTimeApi/<path:url>', methods=['GET', 'POST'])
def proxy(url):
    try:
        url = proxy_to_source(url)
        method = requests.post if request.method == 'POST' else requests.get
        resp = method(
            url,
            stream=True,
            data=request.data,
            params=request.args,
            headers=auth_headers
        )
        return resp.content
    except Exception as e:
        log.error(e)
