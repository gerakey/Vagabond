from math import ceil

from datetime import datetime

from flask import make_response, request, jsonify

from vagabond.__main__ import app, db
from vagabond.models import User, Note, Actor
from vagabond.config import config as config
from vagabond.crypto import require_signature



#@app.before_request
#def log_request_info():
#    app.logger.error('Headers: %s', request.headers)
#    app.logger.error('Body: %s', request.get_data())
#    app.logger.error('Full path: %s', request.full_path)



def error(message, code=400):
    return make_response(message, code)



#TODO
def current_timestamp():
    return ''
    #datetime = datetime.utcnow()



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



"""
Returns: ActivityPub actor object
"""
@app.route('/api/v1/actors/<username>')
def route_get_actor_by_username(username):
    actor = db.session.query(Actor).filter_by(username=username.lower()).first()
    return make_response(actor.to_dict(), 200)



@app.route('/api/v1/actors/<username>/outbox')
def route_user_outbox(username):

    username = username.lower()

    actor = db.session.query(Actor).filter_by(username=username).first()
    if not actor:
        return error('Actor not found', 404)
    
    items_per_page = 20
    total_items = db.session.query(Note).filter_by(actor_id=actor.id).count()
    max_page = ceil(total_items / items_per_page)

    output = {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': f'https://{config["domain"]}/api/v1/actors/{username}/outbox',
        'type': 'OrderedCollection',
        'totalItems': total_items,
        'first': f'https://{config["domain"]}/api/v1/actors/{username}/outbox/1',
        'last': f'https://{config["domain"]}/api/v1/actors/{username}/outbox/{max_page}'
    }

    return make_response(output, 200)



#TODO: Proper format for 'published''
@app.route('/api/v1/actors/<username>/outbox/<int:page>')
def route_user_outbox_paginated(username, page):

    actor = db.session.query(Actor).filter_by(username=username.lower()).first()
    notes = db.session.query(Note).filter_by(actor_id=actor.id).paginate(page, 20).items
    api_url = config['api_url']

    orderedItems = []

    for note in notes:
        orderedItems.append(
            {
                'id': f'{api_url}/notes/{note.id}/activity',
                'type': 'Create',
                'actor': f'{api_url}/actors/{actor.username}',
                'to': ['https://www.w3.org/ns/activitystreams#Public'],
                'cc': [f'{api_url}/actors/{actor.username}/followers'],
                'published': note.published,
                'object': {
                    'id': f'https://{config["domain"]}/api/v1/notes/{note.id}',
                    'attributedTo': f'https://{config["domain"]}/api/v1/actors/{actor.username}',
                    'type': 'Note',
                    'content': note.content,
                    'to': ['https://www.w3.org/ns/activitystreams#Public'],
                    'cc': [f'{api_url}/actors/{actor.username}/followers'],
                    'published': note.published
                }
            }
        )

    output = {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': f'https://{config["domain"]}/api/v1/{username}/outbox/{page}',
        'partOf': f'https://mastodon.social/actors/{username}/outbox',
        'type': 'OrderedCollectionPage',
        'prev': f'https://mastodon.social/actors/{username}/outbox/{page-1}',
        'next': f'https://mastodon.social/actors/{username}/outbox/{page+1}',
        'orderedItems': orderedItems
    }

    return make_response(output, 200)



@app.route('/api/v1/actors/<username>/inbox', methods=['GET', 'POST'])
@require_signature
def route_get_actor_inbox(username):

    if request.method == 'GET':
        actor = db.session.query(Actor).filter_by(username=username).first()
        output = {
            '@context': 'https://www.w3.org/ns/activitystreams',
            'id': f'/api/v1/actors/{actor.username}/inbox',
            'type': 'OrderedCollection'
        }
        return make_response(output, 200)
    elif request.method == 'POST':
        return make_response('asdf', 200)



@app.route('/api/v1/notes/<int:id>')
def get_note_by_id(id):
    note = db.session.query(Note).get(id)
    user = db.session.query(User).get(note.author_id)

    output = {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': f'https://{config["domain"]}/api/v1/notes/{id}',
        'attributedTo': f'https://{config["domain"]}/api/v1/actors/{user.username}',
        'type': 'Note',
        'content': note.content,
        'to': ['https://www.w3.org/ns/activitystreams#Public'],
        'published': '2021-01-22T11:43:38Z'
    }

    return make_response(output, 200)


@app.route('/api/v1/notes/<int:id>/activity')
def get_note_activity_by_id(id):
    note = db.session.query(Note).get(id)
    user = db.session.query(User).get(note.author_id)

    output = {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': f'https://{config["domain"]}/api/v1/notes/{id}/activity',
        'actor': f'https://{config["domain"]}/api/v1/actors/{user.username}',
        'type': 'Create',
        'content': note.content,
        'to': ['https://www.w3.org/ns/activitystreams#Public'],
        'published': '2021-01-22T11:43:38Z',
        'object': {

        }
    }

    return make_response(output, 200)



@app.route('/test')
def route_test():

    output = ''

    for _tuple in request.headers:
        key = _tuple[0]
        output += (key + ": ")
        for i in range (1, len(_tuple)):
            output += (_tuple[i] + "[] ")

    
        output += "<br><br>"

    return make_response(output, 200)
