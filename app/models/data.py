from app import db
from sqlalchemy.sql import func
import datetime

class data(db.Model):
    """
    id              : unique identifier
    ups             : ups id from app.models.config
    charge          : charge percentage
    runtime         : estimated runtime on battery in seconds
    input nominal   : nominal ac input voltage
    input_voltage   : ac input voltage
    output_voltage  : ac output voltage
    battery_nominal : nominal battery voltage
    battery_voltage : current battery voltage
    load            : load percentage
    status          : UPS Status (see NUT docs for values)
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, server_default=func.now())
    ups = db.Column(db.Integer)
    charge = db.Column(db.Integer)
    runtime = db.Column(db.Integer)
    input_nominal = db.Column(db.Float)
    input_voltage = db.Column(db.Float)
    output_voltage = db.Column(db.Float)
    battery_nominal = db.Column(db.Float)
    battery_voltage = db.Column(db.Float)
    load = db.Column(db.Float)
    status = db.Column(db.String(10))

    @classmethod
    def trimDB(cls,expiration=7):
        """
        Deletes data entries older than the given amount of days (defaults to 7 days)
        """
        limit = datetime.datetime.now() - datetime.timedelta(days=expiration)
        try:
            cls.query.filter(cls.timestamp <= limit).delete()
            db.session.commit()
            return "OK"
        except Exception as e:
            return e