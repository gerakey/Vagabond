from vagabond.__main__ import db
from vagabond.models import APObject, APObjectType, Activity

class Create(Activity):
    
    id = db.Column(db.ForeignKey('activity.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': APObjectType.CREATE
    }