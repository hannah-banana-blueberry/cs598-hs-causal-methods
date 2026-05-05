from flask import (
    Blueprint, g, redirect, url_for
)

from typing_speed.auth import login_required
from typing_speed.db import get_db

bp = Blueprint('blog', __name__)


@login_required
@bp.route('/')
def index():
    if g.user:
        completed = g.user['completed']
        if completed == 0:
            return redirect(url_for('survey.pretest'))
        elif completed == 1:
            return redirect(url_for('survey.excerpt'))
        elif completed == 2:
            return redirect(url_for('survey.posttest'))
        elif completed == 3:
            return redirect(url_for('survey.demographics'))
        else:
            return redirect(url_for('auth.finish'))

    from flask import request
    recruitment_location = request.args.get('source')
    prolific_pid = request.args.get('PROLIFIC_PID')
    study_id = request.args.get('STUDY_ID')
    session_id = request.args.get('SESSION_ID')
    return redirect(url_for('auth.register', source=recruitment_location,
                            PROLIFIC_PID=prolific_pid, STUDY_ID=study_id,
                            SESSION_ID=session_id))
