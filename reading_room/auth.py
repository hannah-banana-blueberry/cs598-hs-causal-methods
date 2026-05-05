import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from reading_room.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/register')


@bp.route('/', methods=('GET', 'POST'))
def register():
    if g.user:
        return redirect(url_for('blog.index'))

    if request.method == 'POST':
        device_type = request.form['device_type']
        window_width = request.form.get('window_width')
        user_agent = request.form.get('user_agent')
        recruitment_location = request.args.get('source') or "none"
        prolific_pid = request.args.get('PROLIFIC_PID') or "none"
        study_id = request.args.get('STUDY_ID') or "none"
        session_id = request.args.get('SESSION_ID') or "none"

        db = get_db()
        user_id = len(db.execute('SELECT * FROM user', ()).fetchall()) + 1

        try:
            db.execute(
                "INSERT INTO user (consent, completed, device_type, recruitment_location, window_width, user_agent, prolific_pid, study_id, session_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (1, 0, device_type, recruitment_location, window_width, user_agent, prolific_pid, study_id, session_id),
            )
            db.commit()
        except db.IntegrityError:
            flash(f"User {user_id} is already registered.")
            return render_template('auth/register.html', payment="")

        user = db.execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        session.clear()
        session['user_id'] = user['id']
        return redirect(url_for('blog.index'))

    prolific_pid = request.args.get('PROLIFIC_PID')
    if prolific_pid is None:
        payment = "You will be placed in a drawing for 4 $15 gift cards. (Estimated raffle odds: 1/60)"
    else:
        payment = "You will be compensated $2.00 USD."
    return render_template('auth/register.html', payment=payment)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()


@bp.route('/finish', methods=('GET', 'POST'))
def finish():
    if not g.user:
        return redirect(url_for('blog.index'))

    prolific = g.user['prolific_pid'] != "none"
    session.clear()

    if prolific:
        return render_template('auth/finish_prolific.html')
    return render_template('auth/finish.html')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('blog.index'))
        return view(**kwargs)
    return wrapped_view
