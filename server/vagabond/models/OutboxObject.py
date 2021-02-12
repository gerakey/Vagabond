from datetime import datetime
from vagabond.__main__ import db

class OutboxObject(db.Model):
    '''
        Superclass for objects that appear on an actor's outbox.

        All sub-classes MUST implement to_dict() and to_activity().
    '''
    id = db.Column(db.Integer, primary_key=True)
    published = db.Column(db.DateTime, default=datetime.utcnow)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)
    actor = db.relationship('Actor')
