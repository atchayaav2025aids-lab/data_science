from models import db

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    register_number = db.Column(db.String(50), nullable=True)
    department = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(20), nullable=False)  # 1st Year, 2nd Year, 3rd Year, 4th Year
    graduation_year = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.Text, nullable=True)  # Comma-separated or text
    interests = db.Column(db.Text, nullable=True)
    career_goal = db.Column(db.String(255), nullable=True)
    preferred_industry = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<StudentProfile User:{self.user_id} Dept:{self.department}>'
