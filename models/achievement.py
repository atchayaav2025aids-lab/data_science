from models import db

class AlumniAchievement(db.Model):
    __tablename__ = 'alumni_achievements'

    id = db.Column(db.Integer, primary_key=True)
    alumni_id = db.Column(db.Integer, db.ForeignKey('alumni_profiles.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    organization = db.Column(db.String(150), nullable=True)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<AlumniAchievement {self.title} ({self.year})>'
