from src import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    claims = db.relationship('Claim', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Channel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(8), index=True)
    start = db.Column(db.DateTime, index=True, nullable=True)
    claims = db.relationship('Claim', backref='channel', lazy=True)

    def __repr__(self):
        return '<Channel {}>'.format(self.name)


class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'), nullable=False)

    def __repr__(self):
        return '<Claim {}>'.format(self.time)