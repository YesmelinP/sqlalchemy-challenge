# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import datetime, timedelta 
import os

# Database Setup
#################################################

db_path = os.path.join(os.path.dirname(__file__), 'Resources', 'hawaii.sqlite')
# create engine to hawaii.sqlite
engine = create_engine(f"sqlite:///{db_path}")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)


# Flask Setup
#################################################


app= Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def homepage():
    print("Server received request for homepage...")
    return ( f"Welcome to my API! <br/>"
    f"Available Routes:<br/>"
    f'/api/v1.0/precipitation <br/>'
    f'/api/v1.0/stations <br/>'
    f'/api/v1.0/tobs <br/>'
    f'/api/v1.0/<start> <br/>'
    f'/api/v1.0/<start>/<end> <br/>'
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
   
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return the precipitation data for the last year"""
    # Calculate the date 1 year ago from last date in database
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days= 365 )
    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).all()
    #close session
    session.close()
    # Dict with date as the key and prcp as the value
    precipitation_dict = {date: value for date, value in precipitation}
    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of stations from the dataset"""
    # list of stations from the dataset.
    stations = session.query(Measurement.station).distinct().all()
    # Extract station names from the query result
    station_names = [station[0] for station in stations]
    # Close the session
    session.close()
    # Return the JSONified list of station names
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a JSON list of temperature observations for the previous year."""
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days= 365 )
    temp_observation = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= previous_year).all()
    #close session
    session.close()
    # Makes the Query Into a List
    most_active = [tobs[0] for tobs in temp_observation]
    return jsonify(most_active)

@app.route('/api/v1.0/<start>') 
def temperature_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return the following calculations for start: TMIN, TAVG, and TMAX """
      # Return the following calculations for start: TMIN, TAVG, and TMAX
    temperatures = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
     # extract TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    tmin, tmax, tavg = temperatures[0]
    #close session
    session.close()
    return jsonify({"Minimum temperature ": tmin, "Average temperature": tavg, "Maximum temperature": tmax})
    
@app.route('/api/v1.0/<start>/<end>') 
def temperature_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return the following calculations for start/ end: TMIN, TAVG, and TMAX """
      # Return the following calculations for start/end: TMIN, TAVG, and TMAX
    temperatures = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
     # extract TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    tmin, tmax, tavg = temperatures[0]
    #close session
    session.close()
    return jsonify({"Minimum temperature ": tmin, "Average temperature": tavg, "Maximum temperature": tmax})


# @app.route('/api/v1.0/<start>/<end>') 

if __name__ == "__main__":
    app.run(debug=True)

