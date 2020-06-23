from . import db
from datetime import datetime

class Pitch(db.Model):
    __tablename__='pitch'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    pitch = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    comments = db.relationship('Comments', backref='pitch',cascade="all,delete")
    
    @classmethod
    def get_single_pitch(cls, pitch_id):
        pitch = Pitch.query.filter_by(id=pitch_id).first()
        return pitch
    
    # @classmethod
    # def pitches(cls):
    #     pitch = Pitch.query.all()
    #     return pitch

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255))
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitch.id'))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_comments(cls,pitch_id):
        comments=Comments.query.filter_by(pitch_id=pitch_id)
        return comments