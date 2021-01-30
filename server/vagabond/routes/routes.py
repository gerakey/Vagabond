from math import ceil

from datetime import datetime

from flask import make_response, request, jsonify

from vagabond.__main__ import app, db
from vagabond.models import User, Note, Actor
from vagabond.config import config as config
from vagabond.crypto import require_signature



# Use this when you need to do debugging.
#@app.before_request
#def log_request_info():
#    app.logger.error('Headers: %s', request.headers)
#    app.logger.error('Body: %s', request.get_data())
#    app.logger.error('Full path: %s', request.full_path)



def error(message, code=400):
    return make_response(message, code)



# Serves the react app
@app.route('/')
def index():
    return app.send_static_file('index.html')



@app.route('/.well-known/webfinger')
def route_webfinger():
    resource = request.args.get('resource')
    if not resource:
        return error('Invalid request')

    splits = resource.split(':')

    if len(splits) != 2 or splits[0].lower() != 'acct':
        return error('Invalid resource parameter')

    splits = splits[1].split('@')
    if len(splits) != 2:
        return error('Invalid request')

    username = splits[0].lower()
    hostname = splits[1]

    actor = db.session.query(Actor).filter_by(username=username).first()
    if not actor:
        return error('User not found', 404)

    output = {
        'subject': resource,
        'links': [
            {
                'rel': 'self',
                'type': 'application/activity+json',
                'href': f'https://{config["domain"]}/api/v1/actors/{actor.username}'
            },
            {
                'rel': 'http://webfinger.net/rel/profile-page',
                'type': 'text/html',
                'href': f'https://{config["domain"]}/actors/{actor.username}'
            }
        ]
    }


    return make_response(output, 200)
