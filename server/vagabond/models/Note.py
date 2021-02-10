from datetime import datetime

from vagabond.__main__ import db
from vagabond.config import config
from vagabond.util import xsd_datetime

class Note(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    content = db.Column(db.String(1024), nullable=False)
    published = db.Column(db.DateTime, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)
    author = db.relationship('Actor')

    def __init__(self, author, content, published):
        '''
            Author: Actor object or ID of an actor
            Content: String
            Published: datetime.datetime
        '''

        if isinstance(author, int) == False:
            author = author.id

        self.author_id = author
        self.content = content
        self.published = published


    def to_dict(self):

        api_url = config['api_url']

        return {
            '@context': ['https://www.w3.org/ns/activitystreams'],
            'id': f'{api_url}/notes/{self.id}',
            'attributedTo': f'{api_url}/actors/{self.author.username}',
            'type': 'Note',
            'content': self.content,
            'to': ['https://www.w3.org/ns/activitystreams#Public'],
            'summary': None,
            'published': xsd_datetime(self.published)
        }

    def to_activity(self):
        return {
            '@context': 'https://www.w3.org/ns/activitystreams',
            'id': f'https://{config["api_url"]}/notes/{self.id}/activity',
            'type': 'Create',
            'actor': f'https://{config["api_url"]}/actors/{self.author.username}',
            'published': xsd_datetime(self.published),
            'to': ['https://www.w3.org/ns/activitystreams#Public'],
            'cc': [],
            'object': self.to_dict()
        }

