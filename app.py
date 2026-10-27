import os
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from config import Config
from models import db, User, Notification

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this platform feature.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Context Processors for Templates
    @app.context_processor
    def inject_global_data():
        unread_notifications_count = 0
        if current_user.is_authenticated:
            unread_notifications_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        return dict(
            app_name="AlumniConnect",
            app_subtitle="Centralized Alumni Data Management & Engagement Platform",
            unread_notif_count=unread_notifications_count
        )

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.alumni import alumni_bp
    from routes.admin import admin_bp
    from routes.jobs import jobs_bp
    from routes.internships import internships_bp
    from routes.events import events_bp
    from routes.mentorship import mentorship_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(alumni_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(internships_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(mentorship_bp)

    # Error Handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print(" * AlumniConnect App running on http://127.0.0.1:5000")
    app.run(debug=False, host='127.0.0.1', port=5000)
