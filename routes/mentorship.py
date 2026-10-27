from datetime import datetime
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, MentorshipRequest
from utils.helpers import role_required, create_notification

mentorship_bp = Blueprint('mentorship', __name__, url_prefix='/mentorship')

@mentorship_bp.route('/request/<int:alumni_id>', methods=['POST'])
@login_required
@role_required('student')
def send_request(alumni_id):
    alumni_user = User.query.get_or_404(alumni_id)
    if alumni_user.role != 'alumni':
        flash('Invalid alumni selected.', 'danger')
        return redirect(url_for('student.alumni_directory'))

    existing = MentorshipRequest.query.filter_by(student_id=current_user.id, alumni_id=alumni_user.id).first()
    if existing:
        flash('You have already sent a mentorship request to this alumni.', 'warning')
        return redirect(url_for('student.mentorship_requests'))

    message = request.form.get('message', 'Hello, I would like to request your guidance as a mentor.').strip()

    req = MentorshipRequest(
        student_id=current_user.id,
        alumni_id=alumni_user.id,
        message=message,
        status='Pending'
    )
    db.session.add(req)
    db.session.commit()

    # Notify alumni
    create_notification(
        alumni_user.id,
        "New Mentorship Request Received",
        f"Student {current_user.name} has requested mentorship guidance from you.",
        "mentorship"
    )

    flash(f'Mentorship request sent to {alumni_user.name}!', 'success')
    return redirect(url_for('student.mentorship_requests'))

@mentorship_bp.route('/respond/<int:request_id>', methods=['POST'])
@login_required
@role_required('alumni')
def respond_request(request_id):
    req = MentorshipRequest.query.get_or_404(request_id)
    if req.alumni_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('alumni.mentorship_requests'))

    action = request.form.get('action')  # accept, reject, complete
    if action == 'accept':
        req.status = 'Accepted'
        msg = f"Your mentorship request has been ACCEPTED by {current_user.name}! You can now exchange career guidance."
    elif action == 'reject':
        req.status = 'Rejected'
        msg = f"Your mentorship request was not accepted by {current_user.name} at this time."
    elif action == 'complete':
        req.status = 'Completed'
        msg = f"Your mentorship session with {current_user.name} has been marked as Completed."
    else:
        flash('Invalid status action.', 'danger')
        return redirect(url_for('alumni.mentorship_requests'))

    req.responded_at = datetime.utcnow()
    db.session.commit()

    # Notify student
    create_notification(
        req.student_id,
        f"Mentorship Request {req.status}",
        msg,
        "mentorship"
    )

    flash(f'Mentorship request status updated to {req.status}.', 'success')
    return redirect(url_for('alumni.mentorship_requests'))
