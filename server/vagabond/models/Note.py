from datetime import datetime

from vagabond.__main__ import db

class Note(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)
    content = db.Column(db.String(1024), nullable=False)
    author = db.relationship('Actor')
    published = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {

        }