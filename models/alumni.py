from models import db

class AlumniProfile(db.Model):
    __tablename__ = 'alumni_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    graduation_year = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(100), default='B.Tech')
    current_company = db.Column(db.String(150), nullable=True)
    job_title = db.Column(db.String(150), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    experience = db.Column(db.String(50), nullable=True)  # e.g., "3 Years"
    skills = db.Column(db.Text, nullable=True)
    interests = db.Column(db.Text, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    mentorship_available = db.Column(db.Boolean, default=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    profile_verified = db.Column(db.Boolean, default=False)

    # Relationships
    achievements = db.relationship('AlumniAchievement', backref='alumni', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<AlumniProfile User:{self.user_id} Company:{self.current_company}>'
