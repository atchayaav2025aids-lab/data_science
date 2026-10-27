from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Job

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/<int:job_id>')
@login_required
def detail(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('jobs/detail.html', job=job)
