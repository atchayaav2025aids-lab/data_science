from datetime import datetime
from models import db

class MentorshipRequest(db.Model):
    __tablename__ = 'mentorship_requests'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    alumni_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Pending')  # Pending, Accepted, Rejected, Completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    responded_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    student = db.relationship('User', foreign_keys=[student_id], backref='sent_mentorship_requests')
    alumni = db.relationship('User', foreign_keys=[alumni_id], backref='received_mentorship_requests')

    def __repr__(self):
        return f'<MentorshipRequest Student:{self.student_id} Alumni:{self.alumni_id} Status:{self.status}>'
