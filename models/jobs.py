from datetime import datetime
from models import db

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.String(50), nullable=False, default='Full-time')  # Full-time, Part-time, Remote, Contract
    skills_required = db.Column(db.Text, nullable=False)
    application_link = db.Column(db.String(255), nullable=True)
    deadline = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    poster = db.relationship('User', backref='posted_jobs')

    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'


class Internship(db.Model):
    __tablename__ = 'internships'

    id = db.Column(db.Integer, primary_key=True)
    posted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)  # e.g., "3 Months", "6 Months"
    skills_required = db.Column(db.Text, nullable=False)
    application_link = db.Column(db.String(255), nullable=True)
    deadline = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    poster = db.relationship('User', backref='posted_internships')

    def __repr__(self):
        return f'<Internship {self.title} at {self.company}>'
