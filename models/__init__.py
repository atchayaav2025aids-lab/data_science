from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.student import StudentProfile
from models.alumni import AlumniProfile
from models.mentorship import MentorshipRequest
from models.jobs import Job, Internship
from models.events import Event, EventRegistration
from models.announcements import Announcement
from models.notifications import Notification
from models.achievement import AlumniAchievement
