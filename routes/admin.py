from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, StudentProfile, AlumniProfile, MentorshipRequest, Job, Internship, Event, EventRegistration, Announcement, Notification, AlumniAchievement
from utils.helpers import role_required, create_notification
from analytics.dashboard import AnalyticsDashboard

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@role_required('admin')
def dashboard():
    kpis = AnalyticsDashboard.get_kpi_summary()
    recent_students = User.query.filter_by(role='student').order_by(User.created_at.desc()).limit(5).all()
    recent_alumni = User.query.filter_by(role='alumni').order_by(User.created_at.desc()).limit(5).all()
    recent_events = Event.query.order_by(Event.created_at.desc()).limit(3).all()
    return render_template(
        'admin/dashboard.html',
        kpis=kpis,
        recent_students=recent_students,
        recent_alumni=recent_alumni,
        recent_events=recent_events
    )

@admin_bp.route('/students')
@login_required
@role_required('admin')
def students():
    search_q = request.args.get('search', '').strip()
    query = User.query.filter_by(role='student').join(StudentProfile)
    if search_q:
        query = query.filter((User.name.ilike(f'%{search_q}%')) | (User.email.ilike(f'%{search_q}%')) | (StudentProfile.department.ilike(f'%{search_q}%')))
    students_list = query.all()
    return render_template('admin/students.html', students=students_list, search_query=search_q)

@admin_bp.route('/alumni')
@login_required
@role_required('admin')
def alumni():
    search_q = request.args.get('search', '').strip()
    query = User.query.filter_by(role='alumni').join(AlumniProfile)
    if search_q:
        query = query.filter((User.name.ilike(f'%{search_q}%')) | (User.email.ilike(f'%{search_q}%')) | (AlumniProfile.current_company.ilike(f'%{search_q}%')) | (AlumniProfile.department.ilike(f'%{search_q}%')))
    alumni_list = query.all()
    return render_template('admin/alumni.html', alumni=alumni_list, search_query=search_q)

@admin_bp.route('/verify-alumni/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def verify_alumni(user_id):
    user = User.query.get_or_404(user_id)
    if user.alumni_profile:
        user.alumni_profile.profile_verified = not user.alumni_profile.profile_verified
        db.session.commit()
        status_str = "Verified" if user.alumni_profile.profile_verified else "Unverified"
        flash(f'Alumni profile status updated to {status_str} for {user.name}.', 'success')
        create_notification(
            user.id,
            "Profile Verification Update",
            f"Your alumni profile status has been updated to: {status_str}.",
            "general"
        )
    return redirect(url_for('admin.alumni'))

@admin_bp.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own admin account.', 'danger')
        return redirect(url_for('admin.dashboard'))
    
    db.session.delete(user)
    db.session.commit()
    flash(f'User {user.name} ({user.email}) deleted successfully.', 'success')
    return redirect(request.referrer or url_for('admin.dashboard'))

@admin_bp.route('/jobs')
@login_required
@role_required('admin')
def jobs():
    jobs_list = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('admin/jobs.html', jobs=jobs_list)

@admin_bp.route('/delete-job/<int:job_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job posting deleted.', 'success')
    return redirect(url_for('admin.jobs'))

@admin_bp.route('/internships')
@login_required
@role_required('admin')
def internships():
    internships_list = Internship.query.order_by(Internship.created_at.desc()).all()
    return render_template('admin/internships.html', internships=internships_list)

@admin_bp.route('/delete-internship/<int:internship_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_internship(internship_id):
    internship = Internship.query.get_or_404(internship_id)
    db.session.delete(internship)
    db.session.commit()
    flash('Internship posting deleted.', 'success')
    return redirect(url_for('admin.internships'))

@admin_bp.route('/events', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def events():
    if request.method == 'POST':
        event = Event(
            title=request.form.get('title'),
            description=request.form.get('description'),
            event_date=request.form.get('event_date'),
            event_time=request.form.get('event_time'),
            venue=request.form.get('venue'),
            event_type=request.form.get('event_type', 'Alumni Meet'),
            created_by=current_user.id
        )
        db.session.add(event)
        db.session.commit()

        # Notify all users about new event
        all_users = User.query.all()
        for u in all_users:
            create_notification(
                u.id,
                f"New Event: {event.title}",
                f"A new college event '{event.title}' on {event.event_date} has been posted.",
                "event"
            )

        flash('Event created successfully and notifications broadcasted!', 'success')
        return redirect(url_for('admin.events'))

    events_list = Event.query.order_by(Event.created_at.desc()).all()
    return render_template('admin/events.html', events=events_list)

@admin_bp.route('/announcements', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def announcements():
    if request.method == 'POST':
        ann = Announcement(
            title=request.form.get('title'),
            content=request.form.get('content'),
            created_by=current_user.id
        )
        db.session.add(ann)
        db.session.commit()

        # Broadcast notification
        all_users = User.query.all()
        for u in all_users:
            create_notification(
                u.id,
                f"Announcement: {ann.title}",
                ann.content[:100] + "...",
                "general"
            )

        flash('Announcement published and sent to all users!', 'success')
        return redirect(url_for('admin.announcements'))

    announcements_list = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('admin/announcements.html', announcements=announcements_list)

@admin_bp.route('/mentorship')
@login_required
@role_required('admin')
def mentorship():
    requests_list = MentorshipRequest.query.order_by(MentorshipRequest.created_at.desc()).all()
    return render_template('admin/mentorship.html', requests=requests_list)

@admin_bp.route('/achievements')
@login_required
@role_required('admin')
def achievements():
    achievements_list = AlumniAchievement.query.order_by(AlumniAchievement.year.desc()).all()
    return render_template('admin/achievements.html', achievements=achievements_list)

@admin_bp.route('/analytics')
@login_required
@role_required('admin')
def analytics():
    kpis = AnalyticsDashboard.get_kpi_summary()
    charts = AnalyticsDashboard.generate_all_charts()
    return render_template('admin/analytics.html', kpis=kpis, charts=charts)

@admin_bp.route('/settings')
@login_required
@role_required('admin')
def settings():
    return render_template('admin/settings.html')
