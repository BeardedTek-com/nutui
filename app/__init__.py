# External Imports
from flask import Flask, session, redirect
from flask_sqlalchemy import SQLAlchemy
import yaml
from datetime import timedelta

# Internal Imports
from app.helpers.convert import convert

# Flask Setup
app = Flask(__name__)
app.config.from_file('config.json',load=yaml.safe_load)

# Session Setup
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

# Database Setup
db = SQLAlchemy(app)

# Import Blueprints
from app.blueprints.api import api as apiBlueprint
from app.blueprints.ui import ui as uiBlueprint
app.register_blueprint(apiBlueprint)
app.register_blueprint(uiBlueprint)

# Define Templates
@app.template_filter('timezone')
def convertTZ(time,clockFmt=12,Timezone="America/Anchorage"):
        convert.convertTZ(time,clockFmt,Timezone)

@app.route('/')
def nutuiHome():
    return redirect('/ui/all')