from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, AlumniProfile, MentorshipRequest, Job, Internship, Event, EventRegistration, Announcement, AlumniAchievement
from utils.helpers import role_required, create_notification

alumni_bp = Blueprint('alumni', __name__, url_prefix='/alumni')

@alumni_bp.route('/dashboard')
@login_required
@role_required('alumni')
def dashboard():
    profile = current_user.alumni_profile
    if not profile:
        flash('Please complete your professional alumni profile.', 'info')
        return redirect(url_for('alumni.profile'))

    received_requests = MentorshipRequest.query.filter_by(alumni_id=current_user.id).order_by(MentorshipRequest.created_at.desc()).all()
    pending_count = sum(1 for r in received_requests if r.status == 'Pending')
    accepted_count = sum(1 for r in received_requests if r.status == 'Accepted')

    my_jobs = Job.query.filter_by(posted_by=current_user.id).count()
    my_internships = Internship.query.filter_by(posted_by=current_user.id).count()
    upcoming_events = Event.query.order_by(Event.created_at.desc()).limit(3).all()
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(3).all()

    return render_template(
        'alumni/dashboard.html',
        profile=profile,
        received_requests=received_requests[:5],
        pending_count=pending_count,
        accepted_count=accepted_count,
        my_jobs=my_jobs,
        my_internships=my_internships,
        upcoming_events=upcoming_events,
        announcements=announcements
    )

@alumni_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('alumni')
def profile():
    profile = current_user.alumni_profile
    if request.method == 'POST':
        if not profile:
            profile = AlumniProfile(user_id=current_user.id)
            db.session.add(profile)

        current_user.name = request.form.get('name', current_user.name)
        profile.graduation_year = int(request.form.get('graduation_year', profile.graduation_year or 2022))
        profile.department = request.form.get('department', profile.department)
        profile.degree = request.form.get('degree', profile.degree)
        profile.current_company = request.form.get('current_company', profile.current_company)
        profile.job_title = request.form.get('job_title', profile.job_title)
        profile.industry = request.form.get('industry', profile.industry)
        profile.location = request.form.get('location', profile.location)
        profile.experience = request.form.get('experience', profile.experience)
        profile.skills = request.form.get('skills', profile.skills)
        profile.interests = request.form.get('interests', profile.interests)
        profile.bio = request.form.get('bio', profile.bio)
        profile.linkedin_url = request.form.get('linkedin_url', profile.linkedin_url)
        profile.mentorship_available = True if request.form.get('mentorship_available') else False

        db.session.commit()
        flash('Your professional profile has been updated successfully!', 'success')
        return redirect(url_for('alumni.profile'))

    return render_template('alumni/profile.html', profile=profile)

@alumni_bp.route('/mentorship-requests')
@login_required
@role_required('alumni')
def mentorship_requests():
    requests_list = MentorshipRequest.query.filter_by(alumni_id=current_user.id).order_by(MentorshipRequest.created_at.desc()).all()
    return render_template('alumni/mentorship_requests.html', requests=requests_list)

@alumni_bp.route('/post-job', methods=['GET', 'POST'])
@login_required
@role_required('alumni')
def post_job():
    if request.method == 'POST':
        job = Job(
            posted_by=current_user.id,
            title=request.form.get('title'),
            company=request.form.get('company'),
            description=request.form.get('description'),
            location=request.form.get('location'),
            job_type=request.form.get('job_type', 'Full-time'),
            skills_required=request.form.get('skills_required'),
            application_link=request.form.get('application_link'),
            deadline=request.form.get('deadline')
        )
        db.session.add(job)
        db.session.commit()
        flash('Job posting published successfully!', 'success')
        return redirect(url_for('alumni.my_posts'))

    return render_template('alumni/post_job.html')

@alumni_bp.route('/post-internship', methods=['GET', 'POST'])
@login_required
@role_required('alumni')
def post_internship():
    if request.method == 'POST':
        internship = Internship(
            posted_by=current_user.id,
            title=request.form.get('title'),
            company=request.form.get('company'),
            description=request.form.get('description'),
            location=request.form.get('location'),
            duration=request.form.get('duration', '3 Months'),
            skills_required=request.form.get('skills_required'),
            application_link=request.form.get('application_link'),
            deadline=request.form.get('deadline')
        )
        db.session.add(internship)
        db.session.commit()
        flash('Internship posting published successfully!', 'success')
        return redirect(url_for('alumni.my_posts'))

    return render_template('alumni/post_internship.html')

@alumni_bp.route('/my-posts')
@login_required
@role_required('alumni')
def my_posts():
    jobs = Job.query.filter_by(posted_by=current_user.id).order_by(Job.created_at.desc()).all()
    internships = Internship.query.filter_by(posted_by=current_user.id).order_by(Internship.created_at.desc()).all()
    return render_template('alumni/my_posts.html', jobs=jobs, internships=internships)

@alumni_bp.route('/events')
@login_required
@role_required('alumni')
def events():
    event_list = Event.query.order_by(Event.created_at.desc()).all()
    user_registrations = [er.event_id for er in EventRegistration.query.filter_by(user_id=current_user.id).all()]
    return render_template('alumni/events.html', events=event_list, user_registrations=user_registrations)

@alumni_bp.route('/announcements')
@login_required
@role_required('alumni')
def announcements():
    announcement_list = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('alumni/announcements.html', announcements=announcement_list)

@alumni_bp.route('/achievements', methods=['GET', 'POST'])
@login_required
@role_required('alumni')
def achievements():
    profile = current_user.alumni_profile
    if request.method == 'POST':
        ach = AlumniAchievement(
            alumni_id=profile.id,
            title=request.form.get('title'),
            description=request.form.get('description'),
            organization=request.form.get('organization'),
            year=int(request.form.get('year', 2024))
        )
        db.session.add(ach)
        db.session.commit()
        flash('Achievement added successfully!', 'success')
        return redirect(url_for('alumni.achievements'))

    achievements_list = AlumniAchievement.query.filter_by(alumni_id=profile.id).order_by(AlumniAchievement.year.desc()).all() if profile else []
    return render_template('alumni/achievements.html', achievements=achievements_list)

@alumni_bp.route('/engagement-stats')
@login_required
@role_required('alumni')
def engagement_stats():
    return render_template('alumni/engagement_stats.html')
