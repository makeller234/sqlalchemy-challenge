from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np

app = Flask(__name__)


engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

@app.route("/")
def index():
    return(
        f"Available Routes: <br/><br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/startDate <br/>"
        f"/api/v1.0/startDate/endDate"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    """Gets the percipitation data as well as the date from all stations
    for all entries for a year"""
    
    maxDate = engine.execute("select max(date) from measurement")
    date = dt.date(2017,8,23)
    yearago= date-dt.timedelta(days=365)
    
    prcpData = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>yearago).order_by(Measurement.date)

    prcpList = []
    for row in prcpData:
        prcpList.append({"date":row[0], "prcp":row[1]})

    return jsonify(prcpList)

@app.route("/api/v1.0/stations")
def stations():
    """Gets the station name and station ID numbers"""
    stationsData = session.query(Station.name, Station.station)

    stationList =[]
    for row in stationsData:
        stationList.append({"name":row[0], "station":row[1]})

    return jsonify(stationList)

@app.route("/api/v1.0/tobs")
def tobs():
    """Gets the temperature readings from all stations for a year"""

    maxDate = engine.execute("select max(date) from measurement")
    date = dt.date(2017,8,23)
    yearago= date-dt.timedelta(days=365)

    tobsData = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>yearago).order_by(Measurement.date)

    tobsList = []
    for row in tobsData:
        tobsList.append({"date":row[0], "tobs":row[1]})

    return jsonify(tobsList)


@app.route("/api/v1.0/<start>")
def dates(start):
    
    startDate = dt.datetime.strptime(start, '%Y-%m-%d')


    dateData = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date>=startDate).all()

    returnPretty =[]
    for row in dateData:
        returnPretty.append({"Min Temp":row[0], "Avg Temp": row[1], "Max Temp": row[2]})

    return jsonify(returnPretty)

@app.route("/api/v1.0/<start>/<end>")
def startEnd(start, end):
    startDate = dt.datetime.strptime(start, '%Y-%m-%d')
    endDate = dt.datetime.strptime(end, '%Y-%m-%d')

    datesData = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date>=startDate).filter(Measurement.date<=endDate).all()
    
    returnPretty =[]
    for row in datesData:
        returnPretty.append({"Min Temp":row[0], "Avg Temp": row[1], "Max Temp": row[2]})

    
    return jsonify(returnPretty)


if __name__=="__main__":
    app.run(debug=True)