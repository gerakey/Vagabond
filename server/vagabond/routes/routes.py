'''
    Handles all of Vagabond's routing and
    exports numerous decorators useful for routing. 
'''
from flask import make_response, request, session

from cerberus import Validator

from vagabond.__main__ import app, db
from vagabond.models import User, Actor
from vagabond.config import config



def error(message, code=400):
    '''
        Standard error function used to
        give the client a consistent error
        format. Should be used whenever an error
        is intentionally returned by the server. 
    '''
    return make_response(message, code)



def validate(schema):
    '''
        Decorator.

        Validates JSON POST data according to
        the python-cerbeus schema provided
        as an argument. If the data does not
        match the schema or no POST data is
        provided, a 400 BAD REQUEST error is
        thrown.
    '''
    def decorator(f):
        def wrapper(*args, **kwargs):
            if not request.get_json():
                return error('No JSON data provided. Invalid request', 400)

            result = Validator(schema).validate(request.get_json())
            if not result:
                return error('Invalid request', 400)

            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator



def require_signin(f):
    '''
        Decorator.

        Requires that the incoming request's
        associated session has the 'uid' variable set
        to a valid user ID. An associated instance of the
        vagabond.models.User model is then provided to
        the subsequent function as a key word argument. 

    '''
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