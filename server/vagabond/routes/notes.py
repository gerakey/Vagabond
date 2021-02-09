from flask import make_response, jsonify

from vagabond.__main__ import app, db
from vagabond.models import Note, Actor
from vagabond.config import config
from vagabond.util import xsd_datetime
from vagabond.routes import error

@app.route('/api/v1/notes/<int:id>')
def get_note_by_id(id):
    note = db.session.query(Note).get(id)
    if note is None:
        return error('Note not found', 404)
    response = make_response(note.to_dict(), 200)
    response.headers['Content-Type'] = 'application/activity+json'
    return response


@app.route('/api/v1/notes/<int:id>/activity')
def get_note_activity_by_id(id):
    note = db.session.query(Note).get(id)
    actor = db.session.query(Actor).get(note.author_id)
    output = note.to_activity()

    response = make_response(output, 200)
    response.headers['Content-Type'] = 'application/activity+json'
    return response



@app.route('/api/v1/feed')
def route_feed():
    notes = db.session.query(Note).order_by(Note.published.desc()).all()
    output = []
    domain = config['domain']
    for note in notes:
        output.append({
            'content': note.content,
            'handle': f'@{note.author.username}@{domain}',
            'published': note.published
        })
    return make_response(jsonify(output), 200)