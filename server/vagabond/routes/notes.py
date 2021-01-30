from flask import make_response

from vagabond.__main__ import app, db
from vagabond.models import Note, User


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

    response = make_response(output, 200)
    response.headers['Content-Type'] = 'application/activity+json'
    return response


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

    response = make_response(output, 200)
    response.headers['Content-Type'] = 'application/activity+json'
    return response
