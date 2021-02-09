import os
from flask import Flask, render_template, flash, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename


db = SQLAlchemy()


## Application Factory
def create_app ():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object ('config.Config')

    db.init_app(app)

    with app.app_context ():
        from . import routes
        db.create_all()

        app.register_blueprint(routes.bp)

        return app

