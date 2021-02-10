from math import ceil

from datetime import datetime

from flask import make_response, request, jsonify, session

from vagabond.__main__ import app, db
from vagabond.models import User, Note, Actor
from vagabond.config import config as config
from vagabond.crypto import require_signature, signed_request



def error(message, code=400):
    return make_response(message, code)



def require_args_json(required_args):
    def decorator(f):
        def wrapper(*args, **kwargs):
            json = request.get_json()
            for required in required_args:
                if json.get(required) == None:
                    return error('One more more required arugments was not provided.', 400)
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator



def require_signin(f):
    def wrapper(*args, **kwargs):
        
        if 'uid' not in session:
            return error('You must be signed in to perform this operation.')
        else:
            user = db.session.query(User).get(session['uid'])
            if not user: return error('Invalid session.')
            return f(user=user, *args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper



@app.errorhandler(404)
def route_error_404(e):
    return app.send_static_file('index.html')



# Serves the react app
@app.route('/')
def route_index():
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