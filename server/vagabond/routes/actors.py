
from math import ceil

from flask import make_response, request

from vagabond.__main__ import app, db
from vagabond.models import Note, Actor
from vagabond.config import config
from vagabond.crypto import require_signature


"""
Returns: ActivityPub actor object
"""
@app.route('/api/v1/actors/<username>')
def route_get_actor_by_username(username):
    actor = db.session.query(Actor).filter_by(username=username.lower()).first()
    response =  make_response(actor.to_dict(), 200)
    response.headers['Content-Type'] = 'application/activity+json'
    return response



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
        response = make_response(output, 200)
        response.headers['Content-Type'] = 'application/activity+json'
        return response
    elif request.method == 'POST':
        #TODO: Handle incoming POST requesrs in actor inbox.
        return make_response('asdf', 200)
