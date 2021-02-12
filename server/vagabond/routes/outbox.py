from math import ceil

from flask import make_response, request, session

from dateutil.parser import parse

from vagabond.__main__ import app, db
from vagabond.models import Actor, Note, OutboxObject
from vagabond.routes import error, require_signin
from vagabond.config import config
from vagabond.crypto import require_signature



def get_outbox(username):

    username = username.lower()

    actor = db.session.query(Actor).filter_by(username=username).first()
    if not actor:
        return error('Actor not found', 404)

    items_per_page = 20
    total_items = db.session.query(OutboxObject).filter_by(actor_id=actor.id).count()
    max_page = ceil(total_items / items_per_page)
    api_url = config['api_url']

    output = {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': f'{api_url}/actors/{username}/outbox',
        'type': 'OrderedCollection',
        'totalItems': total_items,
        'first': f'{api_url}/actors/{username}/outbox/1',
        'last': f'{api_url}/actors/{username}/outbox/{max_page}'
    }

    response = make_response(output, 200)
    response.headers['Content-Type'] = 'application/activity+json'
    return response


def create_note(actor, user):

    published = parse(request.get_json().get('published'))
    content = request.get_json().get('content')

    new_note = Note(actor, content, published)
    db.session.add(new_note)
    db.session.commit()

    return make_response('', 201)

'''
**kwargs used instead of 'user' argument
to calm down the linter. User argument provided
by require_signin
'''
#TODO: Cerberus validation
@require_signin
def post_outbox_c2s(actor_name, *args, **kwargs):

    user = kwargs['user']

    is_own_outbox = False
    actor = None
    for _actor in user.actors:
        if _actor.username.lower() == actor_name.lower():
            is_own_outbox = True
            actor = _actor
            break

    if not is_own_outbox:
        return error('You can\'t post to the outbox of an actor that isn\'t yours.')

    _type = request.get_json().get('type')
    if _type is None:
        return error('Invalid ActivityPub object type')
    elif _type == 'Note':
        return create_note(actor, user)


    return error('Invalid ActivityPub object type.');



@require_signature
def post_outbox_s2s(actor_name):
    actor = db.session.query(Actor).filter_by(db.func.lower(actor_name) == db.func.lower(Actor.username)).first()



'''
Post requests to an actor's outbox can come from either a C2S or S2S
interaction. Here we determine which type of request is being received
and act accordingly. GET requests are also permitted.
'''
@app.route('/api/v1/actors/<actor_name>/outbox', methods=['GET', 'POST'])
def route_user_outbox(actor_name):

    if request.method == 'GET':
        return get_outbox(actor_name)
    elif request.method == 'POST' and 'uid' in session:
        return post_outbox_c2s(actor_name)
    elif request.method == 'POST' and 'uid' not in session:
        return post_outbox_s2s(actor_name)
    else:
        pass


@app.route('/api/v1/actors/<actor_name>/outbox/<int:page>')
def route_user_outbox_paginated(actor_name, page):

    actor = db.session.query(Actor).filter_by(username=actor_name.lower()).first()
    outbox_objects = db.session.query(OutboxObject).filter_by(actor_id=actor.id).paginate(page, 20).items
    api_url = config['api_url']

    orderedItems = []

    for outbox_object in outbox_objects:
        orderedItems.append(outbox_object.object.to_activity())

    output = {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': f'{api_url}/actors/{actor_name}/outbox/{page}',
        'partOf': f'{api_url}/actors/{actor_name}/outbox',
        'type': 'OrderedCollectionPage',
        'prev': f'{api_url}/actors/{actor_name}/outbox/{page-1}',
        'next': f'{api_url}/actors/{actor_name}/outbox/{page+1}',
        'orderedItems': orderedItems
    }

    response = make_response(output, 200)
    response.headers['Content-Type'] = 'application/activity+json'
    return response