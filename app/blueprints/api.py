# External Imports
from flask import Blueprint, escape, redirect, jsonify, make_response, request
from flask_sqlalchemy import inspect
from sqlalchemy import desc, asc

# Internal Imports
from app.helpers.convert import convert
from app.models.data import data
from app.models.config import config
from app import db

# API Blueprint Setup
api = Blueprint('api',__name__)


@api.route('/api')
def apiHome():
    return jsonify(
                    {
                        "GET": {
                            "/api"                          : "API Information Page",
                            "/api/init"                     : "Init Database",
                            "/api/list/all"                 : "Returns All Configured NUT Server Paramaters",
                            "/api/list/<upsName>"           : "Returns Named NUT Server Parameters",
                            "/api/<upsName>/<var>/<time>"   : "Returns UPS Data"
                        },
                        "POST": {
                            "/api/setup"                    : "Add/modify/delete a UPS Config using JSON POST.  See Docs for more JSON Formatting"
                        }
                    }
                )


@api.route('/api/init')
def apiInitDB():
    """
    Initialize the database
    """
    result = db.create_all()
    return jsonify(
            {
                "InitDB": True,
                "Result": result
            }
        )
@api.route('/api/setup')
def apiSetup():
    """
    Retrieve configuration from database and dump output in JSON
    """
    configData = config.query.all()
    return jsonify(
                    {
                        "Setup":"GET",
                        "Data": configData
                    }
                )

@api.route('/api/setup',methods=['POST'])
def apiSetupPOST():
    """
    POST configuration of a UPS
    There are 3 functions that can called depending on the incoming JSON:
        - add
            Add a new server config.
            {
                "command": "add",
                "data":  # Use values found in models/config.py
                {
                    "param": Value
                }
            }
        - del
            Delete a server config.
            {
                "command": "del",
                "data":
                {
                    "id": int
                }
            }
        - mod
        Modify a server config.
            {
                "command": "mod",
                "data":  # Use values found in models/config.py
                {
                    "param": Value
                }
            }
    """
    return jsonify({"Setup":"POST"})

@api.route('/api/list/<upsName>')
def apiList(upsName):
    """
    Returns JSON of all configured UPS
    """
    return jsonify({"List":upsName})

@api.route('/api/<ups_name>/<var>/<nRecords>')
def apiGetVar(ups_name,var,nRecords,api=True):
    """
    Returns JSON of UPS Data
    var=all:
        - Returns all variables
    var=<value>:
        - Returns the specified value
            - See models/data for possible values
    time=<time string>
        - Returns the specified amount of data using a time string
            - '1m' = last minute
            - '1h' = last hour
            - '1d' = last day
            - '1w' = last week
            - '1M' = last month
            - '1Y' = last year
    """
    if var == "all":
        # TODO
        results = {}
        if nRecords == "all":
            queryResults = data.query.order_by(desc(data.date)).all()
        else:
            queryResults = data.query.order_by(desc(data.date)).limit(int(nRecords)).all()
        rID = 0
        for result in queryResults:
            results[rID] = {
                            "id":result.id,
                            "date": convert.convertTZ(result.date),
                            "charge": result.charge,
                            "runtime": result.runtime/60,
                            "input_voltage": result.input_voltage,
                            "input_nominal": result.input_nominal,
                            "output_voltage": result.output_voltage,
                            "battery_voltage": result.battery_voltage,
                            "load": result.load,
                            "status": result.status
                            }
            rID += 1
        if api:
            return jsonify(results)
        else:
            return results
    else:
        if api:
            return jsonify({ups_name:{var:"value"}})
        else:
            return {ups_name:{var:"value"}}
@api.route('/api/trimdb/<numdays>')
def apiTrimDB(numdays):
    """
    Trims values older than <days> from database
    Returns JSON of error messages or results
    """
    result = data.trimDB(days=numdays)

    return jsonify(
            {
                "TrimDB": numdays,
                "Result": result
            }
        )
@api.route('/api/data/add/<ups>',methods=['POST'])
def apiAddData(ups):
    valueMap = {
        "battery.charge"            : "charge",
        "battery.runtime"           : "runtime",
        "input.voltage"             : "input_voltage",
        "input.voltage.nominal"     : "input_nominal",
        "output.voltage"            : "output_voltage",
        "battery.voltage"           : "battery_voltage",
        "battery.voltage.nominal"   : "battery_nominal",
        "ups.load"                  : "load",
        "ups.status"                : "status"
    }
    
    values = {
        "ups": ups
    }
    contentType = request.headers.get('Content-Type')
    if contentType  == 'application/json':
        Data = request.json
        for param in Data:
            for value in valueMap:
                if param == value:
                    values[valueMap[value]] = Data[value]
        dataAdd = data(
                    ups = values['ups'],
                    charge = values['charge'],
                    runtime = values['runtime'],
                    input_voltage = values['input_voltage'],
                    input_nominal = values['input_nominal'],
                    output_voltage = values['output_voltage'],
                    battery_voltage = values['battery_voltage'],
                    battery_nominal = values['battery_nominal'],
                    load = values['load'],
                    status = values['status']
                    )
        try:
            db.session.add(dataAdd)
            db.session.commit()
            return jsonify({"Result":"OK","Data":str(dataAdd.__dict__)})
        except Exception as e:
            return jsonify({"Result": "Error","Data":str(e)})
    else:
        return make_response(f"Content-Type: '{contentType}' is not supported")
