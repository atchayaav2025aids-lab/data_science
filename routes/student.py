from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, StudentProfile, AlumniProfile, MentorshipRequest, Job, Internship, Event, EventRegistration, Announcement, Notification
from utils.helpers import role_required, create_notification
from ml.recommendation_engine import RecommendationEngine

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@login_required
@role_required('student')
def dashboard():
    profile = current_user.student_profile
    if not profile:
        flash('Please complete your student profile.', 'info')
        return redirect(url_for('student.edit_profile'))

    total_alumni = AlumniProfile.query.count()
    
    # Run ML engine for top recommendations on dashboard
    alumni_list = AlumniProfile.query.filter_by(mentorship_available=True).all()
    recommendations = RecommendationEngine.recommend_mentors(profile, alumni_list, top_n=4)

    pending_requests = MentorshipRequest.query.filter_by(student_id=current_user.id, status='Pending').count()
    available_jobs = Job.query.count()
    available_internships = Internship.query.count()
    upcoming_events = Event.query.order_by(Event.created_at.desc()).limit(3).all()
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(3).all()

    return render_template(
        'student/dashboard.html',
        profile=profile,
        total_alumni=total_alumni,
        recommendations=recommendations,
        pending_requests=pending_requests,
        available_jobs=available_jobs,
        available_internships=available_internships,
        upcoming_events=upcoming_events,
        announcements=announcements
    )

@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('student')
def profile():
    profile = current_user.student_profile
    if request.method == 'POST':
        if not profile:
            profile = StudentProfile(user_id=current_user.id)
            db.session.add(profile)
        
        current_user.name = request.form.get('name', current_user.name)
        profile.register_number = request.form.get('register_number', profile.register_number)
        profile.department = request.form.get('department', profile.department)
        profile.year = request.form.get('year', profile.year)
        profile.graduation_year = int(request.form.get('graduation_year', profile.graduation_year or 2026))
        profile.skills = request.form.get('skills', profile.skills)
        profile.interests = request.form.get('interests', profile.interests)
        profile.career_goal = request.form.get('career_goal', profile.career_goal)
        profile.preferred_industry = request.form.get('preferred_industry', profile.preferred_industry)
        profile.location = request.form.get('location', profile.location)

        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('student.profile'))

    return render_template('student/profile.html', profile=profile)

@student_bp.route('/alumni')
@login_required
@role_required('student')
def alumni_directory():
    search_q = request.args.get('search', '').strip()
    dept_f = request.args.get('department', '').strip()
    year_f = request.args.get('year', '').strip()
    ind_f = request.args.get('industry', '').strip()
    loc_f = request.args.get('location', '').strip()

    query = AlumniProfile.query.join(User)

    if search_q:
        query = query.filter(
            (User.name.ilike(f'%{search_q}%')) |
            (AlumniProfile.current_company.ilike(f'%{search_q}%')) |
            (AlumniProfile.job_title.ilike(f'%{search_q}%')) |
            (AlumniProfile.skills.ilike(f'%{search_q}%'))
        )
    if dept_f:
        query = query.filter(AlumniProfile.department == dept_f)
    if year_f:
        try:
            query = query.filter(AlumniProfile.graduation_year == int(year_f))
        except ValueError:
            pass
    if ind_f:
        query = query.filter(AlumniProfile.industry == ind_f)
    if loc_f:
        query = query.filter(AlumniProfile.location.ilike(f'%{loc_f}%'))

    alumni = query.all()

    departments = ['Artificial Intelligence & Data Science', 'Computer Science & Engineering', 
                   'Electronics & Communication Engineering', 'Electrical & Electronics Engineering', 
                   'Mechanical Engineering', 'Civil Engineering']
    industries = ['Information Technology', 'Software & AI', 'Hardware & Embedded', 'Manufacturing & Automotive', 'Data Analytics', 'Consulting & Finance']
    years = [2018, 2019, 2020, 2021, 2022, 2023, 2024]

    return render_template(
        'student/alumni_directory.html',
        alumni=alumni,
        departments=departments,
        industries=industries,
        years=years,
        selected_dept=dept_f,
        selected_year=year_f,
        selected_ind=ind_f,
        selected_loc=loc_f,
        search_query=search_q
    )

@student_bp.route('/alumni/<int:alumni_id>')
@login_required
@role_required('student')
def alumni_profile(alumni_id):
    alum = AlumniProfile.query.get_or_404(alumni_id)
    existing_request = MentorshipRequest.query.filter_by(student_id=current_user.id, alumni_id=alum.user_id).first()
    return render_template('student/alumni_profile.html', alum=alum, existing_request=existing_request)

@student_bp.route('/recommended-mentors')
@login_required
@role_required('student')
def recommended_mentors():
    profile = current_user.student_profile
    alumni_list = AlumniProfile.query.filter_by(mentorship_available=True).all()
    recommendations = RecommendationEngine.recommend_mentors(profile, alumni_list, top_n=15)
    return render_template('student/recommended_mentors.html', recommendations=recommendations)

@student_bp.route('/mentorship-requests')
@login_required
@role_required('student')
def mentorship_requests():
    requests_list = MentorshipRequest.query.filter_by(student_id=current_user.id).order_by(MentorshipRequest.created_at.desc()).all()
    return render_template('student/mentorship_requests.html', requests=requests_list)

@student_bp.route('/jobs')
@login_required
@role_required('student')
def jobs():
    search_q = request.args.get('search', '').strip()
    job_type_f = request.args.get('job_type', '').strip()
    
    query = Job.query
    if search_q:
        query = query.filter((Job.title.ilike(f'%{search_q}%')) | (Job.company.ilike(f'%{search_q}%')) | (Job.skills_required.ilike(f'%{search_q}%')))
    if job_type_f:
        query = query.filter(Job.job_type == job_type_f)

    job_list = query.order_by(Job.created_at.desc()).all()
    return render_template('student/jobs.html', jobs=job_list, search_query=search_q, selected_type=job_type_f)

@student_bp.route('/internships')
@login_required
@role_required('student')
def internships():
    search_q = request.args.get('search', '').strip()
    query = Internship.query
    if search_q:
        query = query.filter((Internship.title.ilike(f'%{search_q}%')) | (Internship.company.ilike(f'%{search_q}%')) | (Internship.skills_required.ilike(f'%{search_q}%')))
    
    internship_list = query.order_by(Internship.created_at.desc()).all()

    # Use ML recommendation engine for match scores & reasons
    profile = current_user.student_profile
    recommendations = RecommendationEngine.recommend_internships(profile, internship_list, top_n=20)

    return render_template('student/internships.html', recommendations=recommendations, search_query=search_q)

@student_bp.route('/events')
@login_required
@role_required('student')
def events():
    event_list = Event.query.order_by(Event.created_at.desc()).all()
    user_registrations = [er.event_id for er in EventRegistration.query.filter_by(user_id=current_user.id).all()]
    return render_template('student/events.html', events=event_list, user_registrations=user_registrations)

@student_bp.route('/announcements')
@login_required
@role_required('student')
def announcements():
    announcement_list = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('student/announcements.html', announcements=announcement_list)

@student_bp.route('/notifications')
@login_required
@role_required('student')
def notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    # mark as read
    for n in notifs:
        n.is_read = True
    db.session.commit()
    return render_template('student/notifications.html', notifications=notifs)
