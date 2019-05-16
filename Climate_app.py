import numpy as np
import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Save 12 months ago date
twelve_months = '2016-08-23'

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Weather API. Find Weather Information from 2016-08-23 to 2017-08-23!<br/>"
        f"<br/>Available Routes:<br/>"
        f"<br/>/api/v1.0/precipitation<br/>"
        f"- Returns a list of precipitation amounts (inches) for dates within the past year<br/>"
        f"<br/>/api/v1.0/stations<br/>"
        f"- Returns data for the weather stations to include latitude and longitude<br/>"
        f"<br/>/api/v1.0/tobs<br/>"
        f"- Returns a list of observed temperature for a given date from all stations<br/>"
        f"<br/>/api/v1.0/start<br/>"
        f"- Returns temperature min/avg/max for all dates after the defined start date (YYYY-MM-DD)<br/>"
        f"<br/>/api/v1.0/start/end<br/>"
        f"- Returns temperature min/avg/max for date between the specified start and end dates (YYYY-MM-DD)"
    )

#################################################

#precipitation query
@app.route("/api/v1.0/precipitation")
def precipitation():
    precp_results = session.query(Measurement.date, func.avg(Measurement.prcp)).filter(Measurement.date >= twelve_months).group_by(Measurement.date).all()
    dict_results = dict(precp_results)
    return jsonify(dict_results)

#################################################

# station query
@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude).all()
    return jsonify(station_results)

#################################################

# observed temperature query
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= twelve_months).all()
    return jsonify(tobs_results)

#################################################

# start date to 2017-08-23 temperature query
@app.route("/api/v1.0/<start>")
def start(start):
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(start_results)

#################################################

# start to end date temperature query
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end_results)

#################################################

if __name__ == '__main__':
    app.run(debug=True)

