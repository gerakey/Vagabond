from math import ceil

from flask import make_response, request

from vagabond.__main__ import app, db
from vagabond.models import Actor, Note
from vagabond.routes import error
from vagabond.config import config
from vagabond.util import xsd_datetime
from vagabond.crypto import require_signature



def get_outbox(username):

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

    response = make_response(output, 200)
    response.headers['Content-Type'] = 'application/activity+json'
    return response


def post_outbox():
    pass


@app.route('/api/v1/actors/<username>/outbox', methods=['GET', 'POST'])
def route_user_outbox(username):

    if request.method == 'GET':
        return get_outbox(username)
    else:
        return post_outbox()


@app.route('/api/v1/actors/<username>/outbox/<int:page>')
def route_user_outbox_paginated(username, page):

    actor = db.session.query(Actor).filter_by(username=username.lower()).first()
    notes = db.session.query(Note).filter_by(actor_id=actor.id).paginate(page, 20).items
    api_url = config['api_url']

    orderedItems = []

    for note in notes:
        orderedItems.append(note.to_activity())

    output = {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': f'https://{config["domain"]}/api/v1/{username}/outbox/{page}',
        'partOf': f'https://mastodon.social/actors/{username}/outbox',
        'type': 'OrderedCollectionPage',
        'prev': f'https://mastodon.social/actors/{username}/outbox/{page-1}',
        'next': f'https://mastodon.social/actors/{username}/outbox/{page+1}',
        'orderedItems': orderedItems
    }

    response = make_response(output, 200)
    response.headers['Content-Type'] = 'application/activity+json'
    return response