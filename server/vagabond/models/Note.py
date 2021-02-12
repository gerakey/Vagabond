from vagabond.__main__ import db
from vagabond.config import config
from vagabond.util import xsd_datetime
from vagabond.models import OutboxObject

class Note(OutboxObject):
    '''
        Model implementation of an ActivityPub note
    '''
    id = db.Column(db.Integer, db.ForeignKey('outbox_object.id'), primary_key=True)
    content = db.Column(db.String(1024), nullable=False)
    outbox_object = db.relationship('OutboxObject', backref=db.backref('object', uselist=False))

    def __init__(self, actor, content, published=None):
        '''
            Actor: Actor object or ID of an actor
            Content: String
            Published: datetime.datetime; Default=None
        '''

        # Accept either ID or actor object
        if isinstance(actor, int) == False:
            actor = actor.id

        self.actor_id = actor
        self.content = content
        if published is not None:
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

