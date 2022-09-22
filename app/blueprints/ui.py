# External Imports
from flask import Blueprint, escape, redirect, jsonify, make_response, render_template
from flask_sqlalchemy import inspect
from sqlalchemy import desc

# Internal Imports
from app.helpers.convert import convert
from app.models.data import data
from app.blueprints.api import apiGetVar

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
    chartData = apiGetVar(UPS,"all",1,api=False)[0]
    upsData = apiGetVar(UPS,"all",count,api=False)
    data = {
            "CyberPower1000": {
                "4": {
                    "label": "UPS Load",
                    "min": 0,
                    "max": 100,
                    "value": chartData['load'],
                    "valueLabel": "%"
                },
                "5": {
                    "label": "Battery Runtime",
                    "min": 0,
                    "max": 60,
                    "value": chartData['runtime'],
                    "valueLabel": "min"
                },
                "1": {
                    "label": "Battery VDC",
                    "min": 0,
                    "max": 15,
                    "value": chartData['battery_voltage'],
                    "valueLabel": "VDC"
                },
                "2": {
                    "label": "AC Input",
                    "min": 0,
                    "max": 120,
                    "value" : chartData['input_voltage'],
                    "valueLabel" : "VAC"
                },
                "3": {
                    "label": "AC Output",
                    "min": 0,
                    "max": 120,
                    "value": chartData['output_voltage'],
                    "valueLabel": "VAC"
                },
                "6": {
                    "label": "Battery Charge",
                    "min": 0,
                    "max": 100,
                    "value": chartData['charge'],
                    "valueLabel": "%"
                }
            }
    }
    for ups in data:
        if UPS == ups or UPS == "all":
            for dat in data[ups]:
                # Convert data value to a percentage using value/(max-min)
                data[ups][dat]['percent'] = 100*(data[ups][dat]['value']/(data[ups][dat]['max']-data[ups][dat]['min']))
                if data[ups][dat]["valueLabel"] == "VDC":
                    if data[ups][dat]['value'] >= 13:
                        data[ups][dat]['color'] = 'green'
                    elif data[ups][dat]['value'] >= 12:
                        data[ups][dat]['color'] = 'yellow'
                    else:
                        data[ups][dat]['color'] = 'red'

                if data[ups][dat]["valueLabel"] == "VAC":
                    if data[ups][dat]['value'] >= 110:
                        data[ups][dat]['color'] = 'green'
                    elif data[ups][dat]['value'] >= 100:
                        data[ups][dat]['color'] = 'yellow'
                    else:
                        data[ups][dat]['color'] = 'red'

                if data[ups][dat]["valueLabel"] == "%" and "Load" in data[ups][dat]["label"]:
                    if data[ups][dat]['value'] <= 20:
                        data[ups][dat]['color'] = 'green'
                    elif data[ups][dat]['value'] <= 50:
                        data[ups][dat]['color'] = 'yellow'
                    else:
                        data[ups][dat]['color'] = 'red'

                if data[ups][dat]["valueLabel"] == "%" and "Charge" in data[ups][dat]["label"]:
                    if data[ups][dat]['value'] >= 95:
                        data[ups][dat]['color'] = 'green'
                    elif data[ups][dat]['value'] >= 50:
                        data[ups][dat]['color'] = 'yellow'
                    else:
                        data[ups][dat]['color'] = 'red'


                if data[ups][dat]["valueLabel"] == "min":
                    if data[ups][dat]['value'] >= 40:
                        data[ups][dat]['color'] = 'green'
                    elif data[ups][dat]['value'] >= 20:
                        data[ups][dat]['color'] = 'yellow'
                    else:
                        data[ups][dat]['color'] = 'red'
    
    return make_response(render_template('circleCharts.html',upsData=upsData,data=data,date=chartData['date']))