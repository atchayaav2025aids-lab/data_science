from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Internship

internships_bp = Blueprint('internships', __name__, url_prefix='/internships')

@internships_bp.route('/<int:internship_id>')
@login_required
def detail(internship_id):
    internship = Internship.query.get_or_404(internship_id)
    return render_template('internships/detail.html', internship=internship)
