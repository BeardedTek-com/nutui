# External Imports
from flask import Flask, session, redirect, send_from_directory, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os
import markdown

# Internal Imports
from app.helpers.convert import convert

# Flask Setup
app = Flask(__name__)
try:
    app.config.update(
    SECRET_KEY                        = "SECRET_KEY",
    SESSION_COOKIE_NAME               = "nutui_session",
    STATIC_FOLDER                     = "static",
    TEMPLATES_FOLDER                  = "templates",
    DEBUG                             = False,
    TESTING                           = False,
    SQLALCHEMY_DATABASE_URI           = "sqlite:////data/db.sqlite",
    SQLALCHEMY_TRACK_MODIFICATIONS    = False
    )
except:
    pass

# Session Setup
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

# Database Setup
db = SQLAlchemy(app)

# Import Blueprints
from app.blueprints import api
from app.blueprints import ui
app.register_blueprint(api.api)
app.register_blueprint(ui.ui)

# Initialize the Datbase
db.create_all()

# Define Templates
@app.template_filter('timezone')
def convertTZ(time,clockFmt=12,Timezone="America/Anchorage"):
        convert.convertTZ(time,clockFmt,Timezone)

@app.route('/')
def nutuiHome():
    return redirect('/ui/all')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
@app.route('/license')
def license():
    APP_PATH = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(APP_PATH,'static/docs/license.txt')) as license:
        licensemd = markdown.markdown(license.read(),extensions=["fenced_code"])
    return make_response(render_template('markdown.html',markdown=str(licensemd)))