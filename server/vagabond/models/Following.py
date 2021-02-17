from vagabond.__main__ import db


class Following(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(32), unique=False, nullable=False)
    approved = db.Column(db.Boolean, unique=False, nullable=False)
    hostname = db.Column(db.String(100), unique=False, nullable=False)
    leader = db.Column(db.String(100), unique=True, nullable=False)
    next_page = db.Column(db.String(100), unique=True, nullable=False)

    follower_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable=False)
    follower = db.relationship('Actor', backref='following', foreign_keys=[follower_id])

    def __init__(self, id, follower_id, username, approved, hostname, leader, next_page):
        self.id = id
        self.username = username.lower()
        self.approved = approved
        self.hostname = hostname.lower()
        self.leader = leader.lower()
        self.next_page = next_page.lower()
        self.follower_id = follower_id