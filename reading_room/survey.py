from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from reading_room.auth import login_required
from reading_room.db import get_db
from reading_room.excerpts import get_excerpt

bp = Blueprint('survey', __name__, url_prefix='/survey')


def advance_progress():
    db = get_db()
    db.execute(
        'UPDATE user SET completed = completed + 1 WHERE id = ?',
        (g.user['id'],)
    )
    db.commit()


def require_progress(expected):
    """Redirect to index if user isn't at the expected progress step."""
    if not g.user:
        return redirect(url_for('blog.index'))
    if g.user['completed'] != expected:
        return redirect(url_for('blog.index'))
    return None


@login_required
@bp.route('/pretest', methods=('GET', 'POST'))
def pretest():
    redir = require_progress(0)
    if redir:
        return redir

    if request.method == 'POST':
        fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']
        values = {f: request.form.get(f) for f in fields}

        if any(v is None or v == '' for v in values.values()):
            flash('Please complete all questions before continuing.')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO pre_survey (user_id, q1, q2, q3, q4, q5, q6) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (g.user['id'], *values.values())
            )
            db.commit()
            advance_progress()
            return redirect(url_for('blog.index'))

    return render_template('study/pretest.html')


@login_required
@bp.route('/excerpt', methods=('GET', 'POST'))
def excerpt():
    redir = require_progress(1)
    if redir:
        return redir

    if request.method == 'POST':
        advance_progress()
        return redirect(url_for('blog.index'))

    excerpt_data = get_excerpt()
    return render_template('study/excerpt.html', excerpt=excerpt_data)


@login_required
@bp.route('/posttest', methods=('GET', 'POST'))
def posttest():
    redir = require_progress(2)
    if redir:
        return redir

    if request.method == 'POST':
        fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']
        values = {f: request.form.get(f) for f in fields}

        if any(v is None or v == '' for v in values.values()):
            flash('Please complete all questions before continuing.')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post_survey (user_id, q1, q2, q3, q4, q5, q6) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (g.user['id'], *values.values())
            )
            db.commit()
            advance_progress()
            return redirect(url_for('blog.index'))

    return render_template('study/posttest.html')


@login_required
@bp.route('/demographics', methods=('GET', 'POST'))
def demographics():
    redir = require_progress(3)
    if redir:
        return redir

    if request.method == 'POST':
        q1 = request.form.getlist('q1')
        q1 = ' '.join(q1)
        q2 = request.form.get('q2')
        q2text = request.form.get('q2text')
        q3 = request.form.get('q3')
        q3text = request.form.get('q3text')
        q4 = request.form.get('q4')
        q4text = request.form.get('q4text')
        q5 = request.form.get('q5')
        q6 = request.form.get('q6')
        q6text = request.form.get('q6text')
        q7 = request.form.get('q7')
        q8 = request.form.get('q8')
        email = request.form.get('email')

        error = None
        for field in [q2, q3, q4, q5, q6, q7, q8]:
            if not field:
                error = 'Please complete the survey before continuing.'
                break

        if error is None:
            db = get_db()
            db.execute(
                'INSERT INTO demographics (user_id, q1, q2, q2text, q3, q3text, q4, q4text, q5, q6, q6text, q7, q8, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (g.user['id'], q1, q2, q2text, q3, q3text, q4, q4text, q5, q6, q6text, q7, q8, email)
            )
            db.commit()
            advance_progress()
            return redirect(url_for('auth.finish'))

        flash(error)

    prolific = "true" if g.user['prolific_pid'] != "none" else "false"
    return render_template('study/demographics.html', prolific=prolific)
