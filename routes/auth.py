from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, StudentProfile, AlumniProfile
from utils.helpers import create_notification

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'student':
            return redirect(url_for('student.dashboard'))
        elif current_user.role == 'alumni':
            return redirect(url_for('alumni.dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
    return render_template('index.html')

@auth_bp.route('/about')
def about():
    return render_template('about.html')

@auth_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    return redirect(url_for('auth.index'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash('Invalid email address or password. Please check your credentials.', 'danger')
            return render_template('login.html')

        if not user.is_active:
            flash('Your account has been deactivated. Please contact administrator.', 'danger')
            return render_template('login.html')

        login_user(user, remember=remember)
        flash(f'Welcome back, {user.name}!', 'success')

        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)

        if user.role == 'student':
            return redirect(url_for('student.dashboard'))
        elif user.role == 'alumni':
            return redirect(url_for('alumni.dashboard'))
        elif user.role == 'admin':
            return redirect(url_for('admin.dashboard'))

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'student')
        department = request.form.get('department', 'Artificial Intelligence & Data Science')

        # Validation
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email address already exists.', 'warning')
            return render_template('register.html')

        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # to get user.id

        if role == 'student':
            reg_num = request.form.get('register_number', '')
            year = request.form.get('year', '3rd Year')
            grad_year = int(request.form.get('graduation_year', 2026))
            skills = request.form.get('skills', 'Python, SQL, Machine Learning')
            interests = request.form.get('interests', 'Data Science, Artificial Intelligence')
            career_goal = request.form.get('career_goal', 'Data Scientist')
            preferred_ind = request.form.get('preferred_industry', 'Information Technology')
            location = request.form.get('location', 'Chennai, Tamil Nadu')

            student = StudentProfile(
                user_id=user.id,
                register_number=reg_num,
                department=department,
                year=year,
                graduation_year=grad_year,
                skills=skills,
                interests=interests,
                career_goal=career_goal,
                preferred_industry=preferred_ind,
                location=location
            )
            db.session.add(student)

        elif role == 'alumni':
            grad_year = int(request.form.get('graduation_year', 2022))
            degree = request.form.get('degree', 'B.Tech')
            company = request.form.get('current_company', 'TCS')
            job_title = request.form.get('job_title', 'Software Engineer')
            industry = request.form.get('industry', 'Information Technology')
            location = request.form.get('location', 'Bengaluru')
            experience = request.form.get('experience', '3 Years')
            skills = request.form.get('skills', 'Python, Java, Cloud Computing, SQL')
            interests = request.form.get('interests', 'Mentoring, Software Engineering, AI')
            bio = request.form.get('bio', 'Passionate software engineer eager to guide students.')
            linkedin = request.form.get('linkedin_url', 'https://linkedin.com')

            alumni = AlumniProfile(
                user_id=user.id,
                graduation_year=grad_year,
                department=department,
                degree=degree,
                current_company=company,
                job_title=job_title,
                industry=industry,
                location=location,
                experience=experience,
                skills=skills,
                interests=interests,
                bio=bio,
                linkedin_url=linkedin,
                mentorship_available=True,
                profile_verified=True # auto-verify seeded & newly registered users for demo convenience
            )
            db.session.add(alumni)

        db.session.commit()

        create_notification(
            user.id,
            "Welcome to AlumniConnect!",
            f"Hello {user.name}, welcome to AlumniConnect - Centralized Alumni Platform.",
            "general"
        )

        login_user(user)
        flash('Registration successful! Welcome to AlumniConnect.', 'success')

        if role == 'student':
            return redirect(url_for('student.dashboard'))
        elif role == 'alumni':
            return redirect(url_for('alumni.dashboard'))

    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
