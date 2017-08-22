from gevent import monkey; monkey.patch_all()

import time
import os
import requests
from gevent.pywsgi import WSGIServer
from flask import Flask, Response, request, jsonify, abort

app = Flask(__name__)

# URL format: <protocol>://<username>:<password>@<hostname>:<port>, example: https://test:1234@localhost:9981
config = {
    'bindAddr': os.environ.get('TVH_BINDADDR') or '',
    'tvhURL': os.environ.get('TVH_URL') or 'http://test:test@localhost:9981',
    'tvhProxyURL': os.environ.get('TVH_PROXY_URL') or 'http://localhost',
    'tunerCount': os.environ.get('TVH_TUNER_COUNT') or 6,  # number of tuners in tvh
    'tvhWeight': os.environ.get('TVH_WEIGHT') or 300,  # subscription priority
    'chunkSize': os.environ.get('TVH_CHUNK_SIZE') or 1024*1024,  # usually you don't need to edit this
    'streamProfile': os.environ.get('TVH_PROFILE') or 'pass'  # specifiy a stream profile that you want to use for adhoc transcoding in tvh, e.g. mp4
}


@app.route('/discover.json')
def discover():
    return jsonify({
        'FriendlyName': 'tvhProxy',
        'ModelNumber': 'HDTC-2US',
        'FirmwareName': 'hdhomeruntc_atsc',
        'TunerCount': int(config['tunerCount']),
        'FirmwareVersion': '20150826',
        'DeviceID': '12345678',
        'DeviceAuth': 'test1234',
        'BaseURL': '%s' % config['tvhProxyURL'],
        'LineupURL': '%s/lineup.json' % config['tvhProxyURL']
    })


@app.route('/lineup_status.json')
def status():
    return jsonify({
        'ScanInProgress': 0,
        'ScanPossible': 1,
        'Source': "Cable",
        'SourceList': ['Cable']
    })


@app.route('/lineup.json')
def lineup():
    lineup = []

    for c in _get_channels():
        if c['enabled']:
            url = '%s/stream/channel/%s?profile=%s&weight=%s' % (config['tvhURL'], c['uuid'], config['streamProfile'],int(config['tvhWeight']))

            lineup.append({'GuideNumber': str(c['number']),
                           'GuideName': c['name'],
                           'URL': url
                           })

    return jsonify(lineup)


@app.route('/lineup.post')
def lineup_post():
    return ''


def _get_channels():
    url = '%s/api/channel/grid?start=0&limit=999999' % config['tvhURL']

    try:
        r = requests.get(url)
        return r.json()['entries']

    except Exception as e:
        print('An error occured: ' + repr(e))


if __name__ == '__main__':
    http = WSGIServer((config['bindAddr'], 5004), app.wsgi_app)
    http.serve_forever()
