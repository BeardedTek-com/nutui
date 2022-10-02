# External Imports
from flask import Blueprint, escape, redirect, jsonify, make_response, render_template
from flask_sqlalchemy import inspect
from sqlalchemy import desc
import os

# Internal Imports
from app.helpers.convert import convert
from app.models.data import data
from app.blueprints.api import apiGetVar
from app.helpers.charts import CircleCharts

# API Blueprint Setup
ui = Blueprint('ui',__name__)

@ui.route('/ui')
def uiHome():
    return redirect('/ui/all/60')

@ui.route('/ui/<UPS>')
def uiUPSMain(UPS):
    return redirect(f'/ui/{UPS}/60')

@ui.route('/ui/<UPS>/<count>')
def uiCharts(UPS,count):
    charts = CircleCharts(UPS,count)
    return make_response(charts.response())