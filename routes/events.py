from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Event, EventRegistration
from utils.helpers import create_notification

events_bp = Blueprint('events', __name__, url_prefix='/events')

@events_bp.route('/register/<int:event_id>', methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)
    existing = EventRegistration.query.filter_by(event_id=event.id, user_id=current_user.id).first()
    if existing:
        flash('You are already registered for this event.', 'info')
    else:
        reg = EventRegistration(event_id=event.id, user_id=current_user.id)
        db.session.add(reg)
        db.session.commit()
        flash(f'Successfully registered for "{event.title}"!', 'success')
        create_notification(
            current_user.id,
            f"Event Registration Confirmed",
            f"You have registered for '{event.title}' scheduled on {event.event_date} at {event.event_time}.",
            "event"
        )
    return redirect(request.referrer or url_for('student.events'))
