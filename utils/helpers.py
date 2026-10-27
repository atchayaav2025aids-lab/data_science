from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user
from models import db, Notification

def role_required(*roles):
    """
    Decorator to restrict route access based on user role (student, alumni, admin).
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in roles:
                flash('Access denied. You do not have permission to view this page.', 'danger')
                if current_user.role == 'student':
                    return redirect(url_for('student.dashboard'))
                elif current_user.role == 'alumni':
                    return redirect(url_for('alumni.dashboard'))
                elif current_user.role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                return redirect(url_for('auth.login'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def create_notification(user_id, title, message, notification_type='general'):
    """
    Utility function to create and save a notification for a user.
    """
    try:
        notif = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type
        )
        db.session.add(notif)
        db.session.commit()
        return notif
    except Exception as e:
        db.session.rollback()
        print(f"Error creating notification: {e}")
        return None
