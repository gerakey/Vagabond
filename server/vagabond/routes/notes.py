from flask import make_response

from vagabond.__main__ import app, db
from vagabond.models import Note, Actor
from vagabond.config import config
from vagabond.util import xsd_datetime

@app.route('/api/v1/notes/<int:id>')
def get_note_by_id(id):
    note = db.session.query(Note).get(id)
    response = make_response(note.to_dict(), 200)
    response.headers['Content-Type'] = 'application/activity+json'
    return response


@app.route('/api/v1/notes/<int:id>/activity')
def get_note_activity_by_id(id):
    note = db.session.query(Note).get(id)
    actor = db.session.query(Actor).get(note.actor_id)
    output = note.to_activity()

    response = make_response(output, 200)
    response.headers['Content-Type'] = 'application/activity+json'
    return response
