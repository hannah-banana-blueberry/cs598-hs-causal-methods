from flask import (
    Blueprint, render_template
)

from typing_speed.db import get_db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/', methods=('GET',))
def dashboard():
    counts = get_users_counts()
    return render_template('dashboard.html', counts=counts)


def get_users_counts():
    db = get_db()
    users = db.execute(
        'SELECT u.id, u.completed, u.prolific_pid FROM user u'
    ).fetchall()
    counts = {
        "registered_user_count": 0,
        "completed_user_count": 0,
        "prolific_registered_user_count": 0,
        "prolific_completed_user_count": 0,
    }
    for u in users:
        counts['registered_user_count'] += 1
        if u['prolific_pid'] != "none":
            counts['prolific_registered_user_count'] += 1
        if u['completed'] >= 4:
            counts['completed_user_count'] += 1
            if u['prolific_pid'] != "none":
                counts['prolific_completed_user_count'] += 1
    return counts
