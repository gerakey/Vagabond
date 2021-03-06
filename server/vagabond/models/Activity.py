from vagabond.__main__ import db
from vagabond.models import APObject, APObjectType, Actor
from vagabond.config import config

class Activity(APObject):
    id = db.Column(db.Integer, db.ForeignKey('ap_object.id'), primary_key=True)

    internal_object_id = db.Column(db.ForeignKey('ap_object.id'))
    external_object_id = db.Column(db.String(1024))
    internal_actor_id = db.Column(db.ForeignKey('actor.id'))
    external_actor_id = db.Column(db.String(1024))
    
    actor = db.relationship('Actor', foreign_keys=[internal_actor_id]) #Person performing the activity
    object = db.relationship('APObject', foreign_keys=internal_object_id, uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': APObjectType.ACTIVITY,
        'inherit_condition': id == APObject.id
    }


    def set_object(self, obj):
        '''
            Input: vagabond.models.APObject | str | dict

            Takes an instance of APObject, a URL representing the object,
            or a dictionary representing the object and wraps this instance
            of Activity around it.
        '''
        if isinstance(obj, db.Model):
            self.internal_object_id = obj.id
        elif isinstance(obj, str):
            self.external_object_id = obj
        elif isinstance(obj, dict) and 'id' in obj:
            self.external_object_id = obj['id']
        else:
            raise Exception('Activity#set_object method requires an APObject, a string, or a dictionary')
        

    def set_actor(self, actor):
        '''
            Input: vagabond.models.Actor | str | dict
        '''
        if isinstance(actor, db.Model):
            self.internal_actor_id = actor.id
        elif isinstance(actor, str):
            self.external_actor_id = actor
        elif isinstance(actor, dict) and 'id' in actor:
            self.external_actor_id = actor['id']
        else:
            raise Exception('Activity#set_actor method requires an Actor, a string, or a dictionary')


    def to_dict(self):
        output = super().to_dict()

        if self.object is not None:
            output['object'] = self.object.to_dict()
        elif self.external_object_id is not None:
            output['object'] = self.external_object_id
        else:
            raise Exception('Activites must have an internal or external object.')

        if self.internal_actor_id is not None:
            output['actor'] = f'{config["api_url"]}/actors/{self.actor.username}'
        elif self.external_actor_id is not None:
            output['actor'] = self.external_actor_id
        else:
            raise Exception('Activies must have an internal or external actor')

        return output