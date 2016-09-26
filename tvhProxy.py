import time

from flask import Flask, Response, request, jsonify, abort
import requests

app = Flask(__name__)

# URL format: <protocol>://<username>:<password>@<hostname>:<port>, example: https://test:1234@localhost:9981
config = {
    'tvhURL': 'http://test:test@127.0.0.1:9981',
    'tvhProxyURL': 'http://127.0.0.1',
    'tvhProxyPort': 5004,  # do _NOT_ change this.
    'debug': True
}


@app.route('/discover.json')
def discover():
    return jsonify({
        'FriendlyName': 'tvhProxy',
        'ModelNumber': 'HDTC-2US',
        'FirmwareName': 'hdhomeruntc_atsc',
        'FirmwareVersion': '20150826',
        'DeviceID': '12345678',
        'DeviceAuth': 'test1234',
        'BaseURL': '%s:%s' % (config['tvhProxyURL'], config['tvhProxyPort']),
        'LineupURL': '%s:%s/lineup.json' % (config['tvhProxyURL'], config['tvhProxyPort'])
    })


@app.route('/lineup_status.json')
def status():
    return jsonify({
        'ScanInProgress': 0,
        'ScanPossible': 1,
        'Source': "Cable",
        'SourceList': ['Antenna', 'Cable']
    })


@app.route('/lineup.json')
def lineup():
    lineup = []

    for c in _get_channels():
        if c['enabled']:
            url = '%s%s%s' % (config['tvhProxyURL'], '/auto/v', c['number'])

            lineup.append({'GuideNumber': str(c['number']),
                           'GuideName': c['name'],
                           'URL': url
                           })

    return jsonify(lineup)


@app.route('/auto/<channel>')
def stream(channel):
    url = ''
    channel = channel.replace('v', '')

    if not request.args.get('duration'):
        duration = 60 * 60  # set default timeout to 1h if not set
    else:
        duration = int(request.args.get('duration'))
    duration = time.time() + duration

    for c in _get_channels():
        if c['number'] == int(channel):
            url = '%s%s%s' % (config['tvhURL'], '/stream/channel/', c['uuid'])

    if not url:
        abort(404)
    else:
        req = requests.get(url, stream=True)

        def generate():
            while True:
                for chunk in req.iter_content(chunk_size=4096):
                    if time.time() < duration:
                        yield chunk
                    else:
                        break

        return Response(generate(), content_type=req.headers['content-type'])


def _get_channels():
    url = config['tvhURL'] + '/api/channel/grid?start=0&limit=999999'

    try:
        r = requests.get(url)
        return r.json()['entries']

    except Exception as e:
        print('An error occured: ' + repr(e))


if __name__ == '__main__':
    app.run(debug=config['debug'], host='0.0.0.0', port=config['tvhProxyPort'], threaded=True)
