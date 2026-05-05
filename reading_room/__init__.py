import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev1',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .reading_room import db
    db.init_app(app)

    from .reading_room import auth
    app.register_blueprint(auth.bp)

    from .reading_room import blog
    app.register_blueprint(blog.bp)

    from .reading_room import survey
    app.register_blueprint(survey.bp)

    from .reading_room import dashboard
    app.register_blueprint(dashboard.bp)

    return app
