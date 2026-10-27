import unittest
from app import create_app
from models import db, User, StudentProfile, AlumniProfile
from analytics.dashboard import AnalyticsDashboard

from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class TestAlumniConnect(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        with self.app.app_context():
            db.create_all()
            if not User.query.filter_by(email="admin@alumniconnect.com").first():
                admin = User(name="System Administrator", email="admin@alumniconnect.com", role="admin")
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()
        self.client = self.app.test_client()

    def test_01_landing_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AlumniConnect', response.data)
        print("[PASS] Landing page loads successfully.")

    def test_02_admin_login(self):
        res_admin = self.client.post('/login', data={'email': 'admin@alumniconnect.com', 'password': 'admin123'}, follow_redirects=True)
        self.assertEqual(res_admin.status_code, 200)
        self.assertIn(b'Admin Dashboard', res_admin.data)
        print("[PASS] Admin authentication working.")

    def test_03_student_registration_and_flow(self):
        # Register new student
        reg_res = self.client.post('/register', data={
            'name': 'New Student',
            'email': 'newstudent@college.edu',
            'password': 'password123',
            'role': 'student',
            'department': 'Artificial Intelligence & Data Science'
        }, follow_redirects=True)
        self.assertEqual(reg_res.status_code, 200)
        self.assertIn(b'Student Control Center', reg_res.data)
        print("[PASS] Student registration & dashboard flow working.")

    def test_04_alumni_registration_and_flow(self):
        # Register new alumni
        reg_res = self.client.post('/register', data={
            'name': 'New Alumni',
            'email': 'newalumni@college.edu',
            'password': 'password123',
            'role': 'alumni',
            'department': 'Computer Science & Engineering'
        }, follow_redirects=True)
        self.assertEqual(reg_res.status_code, 200)
        self.assertIn(b'Alumni Portal', reg_res.data)
        print("[PASS] Alumni registration & dashboard flow working.")

    def test_05_plotly_analytics(self):
        with self.app.app_context():
            charts = AnalyticsDashboard.generate_all_charts()
            self.assertEqual(len(charts), 10)
        print("[PASS] All 10 Plotly interactive analytics charts generated without errors.")

if __name__ == '__main__':
    unittest.main()
