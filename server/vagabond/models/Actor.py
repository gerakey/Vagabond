from vagabond.__main__ import db
from vagabond.config import config
from Crypto.PublicKey import RSA

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    public_key = db.Column(db.Text(16639)) #PEM format
    private_key = db.Column(db.Text(16639)) #PEM format
    username = db.Column(db.String(32), nullable=False)
    user = db.relationship('User')
    notes = db.relationship('Note')

    def __init__(self, *args, **kwargs):
        if kwargs.get('user_id') != None:
            self.user_id = kwargs.get('user_id')
        elif kwargs.get('user') != None:
            self.user_id = user.id
        else:
            raise Exception('Instantiating an Actor requires either a user object or user id. ')

        if kwargs.get('username') != None:
            self.username = kwargs.get('username')
        
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.public_key().export_key()


    def to_dict(self):

        api_url = config['api_url']
        username = self.username

        return {
            '@context': [
                'https://www.w3.org/ns/activitystreams',
                'https://w3id.org/security/v1'
                ],
            'id': f'{api_url}/actors/{username}',
            'type': 'Person',
            'inbox': f'{api_url}/actors/{username}/inbox',
            'outbox': f'{api_url}/actors/{username}/outbox',
            'followers': f'{api_url}/actors/{username}/followers',
            'following': f'{api_url}/actors/{username}/following',
            'liked': f'{api_url}/actors/{username}/liked',
            'preferredUsername': self.username,
            'publicKey': {
                'actor': f'{api_url}/actors/{username}',
                'id': f'{api_url}/actors/{username}#main-key',
                'publicKeyPem': self.public_key
            }
        }


