from app import db

class config(db.Model):
    """
    id          : unique identifier
    name        : human readable identifier (default = "ups")
    host        : Host to connect to (default = localhost)
    port        : Port where NUT listens to connections (default = 3493)
    login       : Username used to connect to NUT server (default = "")
    password    : Password used for auth (default = "")
    timeout     : Timeout used to wait for network response in seconds (default = 5)
    notes       : Notes related to UPS (default = "")
    hidden      : Hide UPS from main display (default = False)
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),unique=True)
    host = db.Column(db.String(250))
    port = db.Column(db.Integer)
    login = db.Column(db.String(20))
    password = db.Column(db.String(50))
    notes = db.Column(db.Text)
    hidden = db.Column(db.Boolean)
