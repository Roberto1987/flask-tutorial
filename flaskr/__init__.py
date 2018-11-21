import os
import logging
import time
import os.path
import pathlib

from flask import Flask

# Importing other file

from . import auth
from . import blog


################################################
## note: pathlib doesn't work with python 2.7 ##
################################################


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # create and configure the logs
    log_filename = str(time.strftime("flaskr_log_%Y-%m-%d_%H", time.gmtime()))

    create_log(log_filename)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    logging.info('SECRET_KEY=dev')
    logging.info('DATABASE=' + os.path.join(app.instance_path + 'flaskr.sqlite'))

    print('SECRET KEY:' + app.config['SECRET_KEY'])
    print('DATABASE' + app.config['DATABASE'])

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    app.register_blueprint(auth.bp)

    app.register_blueprint(blog.bp)

    app.add_url_rule('/', endpoint='index')

    return app


def create_log(filename):
    log_file_path = pathlib.Path(os.path.abspath('.') + '/' + filename)
    if log_file_path.is_file():
        print('Log file for this hour already exists!')
        filename = filename + 'random_number'
    print('Log file' + filename + 'created')
    logging.basicConfig(filename=filename, level=logging.INFO)
