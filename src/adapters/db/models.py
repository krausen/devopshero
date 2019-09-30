from src.adapters.db import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True)
    claims = db.relationship("Claim", backref="user", lazy=True)

    def __repr__(self):
        return "<User {}>".format(self.user_name)


class ChannelModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.String(8), index=True)
    start = db.Column(db.DateTime, index=True, nullable=True)
    claims = db.relationship("Claim", backref="channel", lazy=True)

    def __repr__(self):
        return "<Channel {}>".format(self.channel_id)


class ClaimModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey("channel.id"), nullable=False)

    def __repr__(self):
        return "<Claim {} by {}>".format(self.time, self.user_id)
