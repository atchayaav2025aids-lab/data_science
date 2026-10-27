from datetime import datetime
from models import db

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.String(50), nullable=False)
    event_time = db.Column(db.String(50), nullable=False)
    venue = db.Column(db.String(150), nullable=False)
    event_type = db.Column(db.String(50), nullable=False, default='Alumni Meet')  # Alumni Meet, Webinar, Technical Talk, Workshop
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship('User', backref='created_events')
    registrations = db.relationship('EventRegistration', backref='event', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Event {self.title} ({self.event_date})>'


class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('event_id', 'user_id', name='_event_user_uc'),)

    def __repr__(self):
        return f'<EventRegistration Event:{self.event_id} User:{self.user_id}>'
