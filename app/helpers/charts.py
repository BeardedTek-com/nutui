from app.blueprints.api import apiGetVar, apiInitDB
from flask import render_template
from sqlalchemy import exc
import logging

class CircleCharts:
    def __init__(self,UPS,count):
        # Logging
        logging.getLogger().setLevel(logging.DEBUG)
        self.UPS = UPS
        self.count = count
        self.chartData = None
    def response(self):
        try:
            # Try to get data from the database
            self.chartData = apiGetVar(self.UPS,"all",1,api=False)[0]
            logging.debug(self.chartData)
            self.upsData = apiGetVar(self.UPS,"all",self.count,api=False)
        except Exception as e:
            self.output = render_template('nodata.html',error=str(e))

        if self.chartData:
            logging.debug(f"chartData:{self.chartData}")
            # Process Chart Data
            self.processChartData()
            # Render the Page
            self.render()
        else:
            error = f"{self.UPS}: No data"
            self.output = render_template('nodata.html',error=str(error))
        # Return page outputy
        return self.output

    def processChartData(self):
        self.charts = {
            "CyberPower1000": {
                "4": {
                    "label": "UPS Load",
                    "min": 0,
                    "max": 100,
                    "value": self.chartData['load'],
                    "valueLabel": "%"
                },
                "5": {
                    "label": "Battery Runtime",
                    "min": 0,
                    "max": 60,
                    "value": self.chartData['runtime'],
                    "valueLabel": "min"
                },
                "1": {
                    "label": "Battery VDC",
                    "min": 0,
                    "max": 15,
                    "value": self.chartData['battery_voltage'],
                    "valueLabel": "VDC"
                },
                "2": {
                    "label": "AC Input",
                    "min": 0,
                    "max": 120,
                    "value" : self.chartData['input_voltage'],
                    "valueLabel" : "VAC"
                },
                "3": {
                    "label": "AC Output",
                    "min": 0,
                    "max": 120,
                    "value": self.chartData['output_voltage'],
                    "valueLabel": "VAC"
                },
                "6": {
                    "label": "Battery Charge",
                    "min": 0,
                    "max": 100,
                    "value": self.chartData['charge'],
                    "valueLabel": "%"
                }
            }
        }

    def render(self):
        for ups in self.charts:
            if self.UPS == ups or self.UPS == "all":
                for dat in self.charts[ups]:
                    # Convert self.charts value to a percentage using value/(max-min)
                    self.charts[ups][dat]['percent'] = 100*(self.charts[ups][dat]['value']/(self.charts[ups][dat]['max']-self.charts[ups][dat]['min']))
                    if self.charts[ups][dat]["valueLabel"] == "VDC":
                        if self.charts[ups][dat]['value'] >= 13:
                            self.charts[ups][dat]['color'] = 'green'
                        elif self.charts[ups][dat]['value'] >= 12:
                            self.charts[ups][dat]['color'] = 'yellow'
                        else:
                            self.charts[ups][dat]['color'] = 'red'

                    if self.charts[ups][dat]["valueLabel"] == "VAC":
                        if self.charts[ups][dat]['value'] >= 110:
                            self.charts[ups][dat]['color'] = 'green'
                        elif self.charts[ups][dat]['value'] >= 100:
                            self.charts[ups][dat]['color'] = 'yellow'
                        else:
                            self.charts[ups][dat]['color'] = 'red'

                    if self.charts[ups][dat]["valueLabel"] == "%" and "Load" in self.charts[ups][dat]["label"]:
                        if self.charts[ups][dat]['value'] <= 20:
                            self.charts[ups][dat]['color'] = 'green'
                        elif self.charts[ups][dat]['value'] <= 50:
                            self.charts[ups][dat]['color'] = 'yellow'
                        else:
                            self.charts[ups][dat]['color'] = 'red'

                    if self.charts[ups][dat]["valueLabel"] == "%" and "Charge" in self.charts[ups][dat]["label"]:
                        if self.charts[ups][dat]['value'] >= 95:
                            self.charts[ups][dat]['color'] = 'green'
                        elif self.charts[ups][dat]['value'] >= 50:
                            self.charts[ups][dat]['color'] = 'yellow'
                        else:
                            self.charts[ups][dat]['color'] = 'red'


                    if self.charts[ups][dat]["valueLabel"] == "min":
                        if self.charts[ups][dat]['value'] >= 40:
                            self.charts[ups][dat]['color'] = 'green'
                        elif self.charts[ups][dat]['value'] >= 20:
                            self.charts[ups][dat]['color'] = 'yellow'
                        else:
                            self.charts[ups][dat]['color'] = 'red'
        self.output = render_template('circleCharts.html',upsData=self.upsData,data=self.charts,date=self.chartData['date'])