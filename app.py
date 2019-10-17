from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precip():

    session = Session(engine)

    all_precip = []

    results = session.query(Measurement.prcp, Measurement.date).limit(15).all()
    for prcp, date in results:
        prcp_dict = {}
        prcp_dict["prcp"] = prcp
        prcp_dict["date"] = date
        all_precip.append(prcp_dict)

    return jsonify(all_precip)


@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<end><br/>"

    )

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    return jsonify(session.query(Station.station).all())

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    max_date = session.query(func.max(Measurement.date))
    f = '%Y-%m-%d'
    max_date = dt.datetime.strptime(max_date[0][0], f)
    one_year = dt.timedelta(days=365)
    one_year_ago = max_date - one_year

    qry = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= one_year_ago.strftime(f)).filter(Measurement.date <= max_date.strftime(f)).order_by(Measurement.date)

    all_precip = []

    for date, prcp in qry:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_precip.append(prcp_dict)

    return jsonify(all_precip)


@app.route("/api/v1.0/<start_date>")
def startd(start_date):
    session = Session(engine)


    """TMIN, TAVG, and TMAX for a list of dates.

    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d

    Returns:
        TMIN, TAVE, and TMAX
    """

    all_temps = []
    qry = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    temp_dict = {}
    temp_dict["TMIN"] = qry[0][0]
    temp_dict["TAVG"] = qry[0][1]
    temp_dict["TMAX"] = qry[0][2]


    return jsonify(temp_dict)


@app.route("/api/v1.0/<start_date>/<end_date>")
def endd(start_date,end_date):

    session = Session(engine)


    """TMIN, TAVG, and TMAX for a list of dates.

    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d

    Returns:
        TMIN, TAVE, and TMAX
    """

    all_temps = []
    qry = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    temp_dict = {}
    temp_dict["TMIN"] = qry[0][0]
    temp_dict["TAVG"] = qry[0][1]
    temp_dict["TMAX"] = qry[0][2]

    return jsonify(temp_dict)


if __name__ == "__main__":
    app.run(debug=True)
