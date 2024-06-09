# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from datetime import datetime, timedelta 


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# View all of the classes that automap found
# Base.classes.keys()
# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement
# Create our session (link) from Python to the DB
session = Session(engine)


# Database Setup
#################################################
app= Flask(__name__)

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

# reflect an existing database into a new model

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation dictionary"""


    return jsonify(precipitation_dict)

# reflect the tables


# Save references to each table


# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################

if __name__ == "__main__":
    app.run(debug=True)




#################################################
# Flask Routes
#################################################
