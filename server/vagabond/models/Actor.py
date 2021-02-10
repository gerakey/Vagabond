from vagabond.__main__ import db
from vagabond.config import config
from Crypto.PublicKey import RSA

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    public_key = db.Column(db.Text(16639))
    private_key = db.Column(db.Text(16639))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='actors', foreign_keys=[user_id])

    def __init__(self, username, user=None, user_id=None):

        self.username = username

        if user_id is not None:
            self.user_id = user_id
        elif user is not None:
            self.user_id = user.id
        else:
            raise Exception('Instantiating an Actor requires either a user object or user id. ')
        
        key = RSA.generate(4096)
        self.private_key = key.export_key()
        self.public_key = key.publickey().export_key()


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


