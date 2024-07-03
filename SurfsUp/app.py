# Import the dependencies
import os
import datetime as dt
import numpy as np
from flask import Flask, jsonify, request, abort
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Database Setup
#################################################
# Define the path to the SQLite database
db_path = os.path.join(os.path.dirname(__file__), 'Resources', 'hawaii.sqlite')

# Create engine to connect to the SQLite database
engine = create_engine(f"sqlite:///{db_path}")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables from the database
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Flask Setup
#################################################
# Initialize the Flask application
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Define the homepage route
@app.route("/")
def homepage():
    """
    List all available API routes.
    """
    return (
        f"Welcome to my API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Define the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """
    Return the precipitation data for the last year.
    """
    # Create a session from Python to the database
    session = Session(engine)
    
    # Calculate the date 1 year ago from the last date in the database
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= previous_year).all()
    
    # Close the session
    session.close()
    
    # Create a dictionary with date as the key and prcp as the value
    precipitation_dict = {date: value for date, value in precipitation}
    
    # Return the JSONified precipitation data
    return jsonify(precipitation_dict)

# Define the stations route
@app.route("/api/v1.0/stations")
def stations():
    """
    Return a list of all stations in the dataset.
    """
    # Create a session from Python to the database
    session = Session(engine)
    
    # Query all stations
    stations = session.query(Station.station).all()
    
    # Close the session
    session.close()
    
    # Extract station names from the query result
    station_names = [station[0] for station in stations]
    
    # Return the JSONified list of station names
    return jsonify(station_names)

# Define the tobs (temperature observations) route
@app.route("/api/v1.0/tobs")
def tobs():
    """
    Return the temperature observations for the most active station (USC00519281)
    for the previous year.
    """
    # Create a session from Python to the database
    session = Session(engine)
    
    # Calculate the date 1 year ago from the last date in the database
    previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query the temperature observations for the most active station for the last year
    temp_observation = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= previous_year).all()
    
    # Close the session
    session.close()
    
    # Extract temperature observations from the query result
    most_active = [tobs[0] for tobs in temp_observation]
    
    # Return the JSONified temperature observations
    return jsonify(most_active)

# Define the temperature route with start date
@app.route('/api/v1.0/<start>')
def temperature_start(start):
    """
    Return the minimum, average, and maximum temperatures for all dates
    greater than or equal to the start date.
    """
    try:
        # Parse the start date from the URL parameter
        start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    except ValueError:
        # Return an error if the date format is invalid
        abort(400, description="Invalid date format. Use YYYY-MM-DD.")
    
    # Create a session from Python to the database
    session = Session(engine)
    
    # Query for the minimum, maximum, and average temperatures from the start date
    temperatures = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    
    # Close the session
    session.close()
    
    # Extract temperature data from the query result
    tmin, tmax, tavg = temperatures[0]
    
    # Return the JSONified temperature data
    return jsonify({"Minimum temperature": tmin, "Average temperature": tavg, "Maximum temperature": tmax})

# Define the temperature route with start and end dates
@app.route('/api/v1.0/<start>/<end>')
def temperature_start_end(start, end):
    """
    Return the minimum, average, and maximum temperatures for all dates
    between the start and end dates.
    """
    try:
        # Parse the start and end dates from the URL parameters
        start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
        end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
    except ValueError:
        # Return an error if the date format is invalid
        abort(400, description="Invalid date format. Use YYYY-MM-DD.")
    
    # Create a session from Python to the database
    session = Session(engine)
    
    # Query for the minimum, maximum, and average temperatures between the start and end dates
    temperatures = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    # Close the session
    session.close()
    
    # Extract temperature data from the query result
    tmin, tmax, tavg = temperatures[0]
    
    # Return the JSONified temperature data
    return jsonify({"Minimum temperature": tmin, "Average temperature": tavg, "Maximum temperature": tmax})

# Define error handlers
@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors.
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    """
    Handle 400 errors.
    """
    return jsonify({"error": error.description}), 400

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
