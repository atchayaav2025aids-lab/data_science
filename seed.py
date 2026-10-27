import os
from app import create_app
from models import db, User, StudentProfile, AlumniProfile

app = create_app()

def initialize_database():
    with app.app_context():
        print("Re-creating clean database with valid login accounts for Admin, Student, and Alumni...")
        db.drop_all()
        db.create_all()

        # 1. Admin Account
        admin = User(name="System Administrator", email="admin@alumniconnect.com", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)

        # 2. Student Account (Valid Login, 0 sample jobs/events/requests)
        student_user = User(name="Student User", email="student@alumniconnect.com", role="student")
        student_user.set_password("student123")
        db.session.add(student_user)
        db.session.flush()

        student_prof = StudentProfile(
            user_id=student_user.id,
            register_number="211421104001",
            department="Artificial Intelligence & Data Science",
            year="3rd Year",
            graduation_year=2026,
            skills="",
            interests="",
            career_goal="",
            preferred_industry="",
            location=""
        )
        db.session.add(student_prof)

        # 3. Alumni Account (Valid Login, 0 sample jobs/events/requests)
        alumni_user = User(name="Alumni User", email="alumni@alumniconnect.com", role="alumni")
        alumni_user.set_password("alumni123")
        db.session.add(alumni_user)
        db.session.flush()

        alumni_prof = AlumniProfile(
            user_id=alumni_user.id,
            graduation_year=2022,
            department="Artificial Intelligence & Data Science",
            degree="B.Tech",
            current_company="Tech Industry",
            job_title="Software Engineer",
            industry="Information Technology",
            location="India",
            experience="3 Years",
            skills="",
            interests="",
            bio="",
            mentorship_available=True,
            linkedin_url="",
            profile_verified=True
        )
        db.session.add(alumni_prof)

        db.session.commit()
        print("\n=======================================================")
        print("ALL 3 LOGIN ACCOUNTS CREATED SUCCESSFULLY!")
        print("0 Jobs | 0 Internships | 0 Events | 0 Requests")
        print("=======================================================")
        print("1. Admin:   admin@alumniconnect.com   / admin123")
        print("2. Student: student@alumniconnect.com / student123")
        print("3. Alumni:  alumni@alumniconnect.com  / alumni123")
        print("=======================================================\n")

if __name__ == '__main__':
    initialize_database()
