#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 09:07:42 2020

@author: carlyfabris
"""

from flask import Flask, jsonify
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
#%%
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#%%
app = Flask(__name__)
#%%

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
    )
#%%
@app.route("/api/v1.0/precipitation")
def precipitation():
    conn = engine.connect()
    most_recent = pd.read_sql("SELECT date FROM measurement GROUP BY date ORDER BY date DESC LIMIT 1", conn)
    most_recent = most_recent['date'][0]
    #print(most_recent)
    one_year_ago = pd.read_sql(f"SELECT DATE('{most_recent}','-1 year') AS Date LIMIT 1", conn)
    one_year_ago = one_year_ago['Date'][0]
    #print(one_year_ago)
    precip_df = pd.read_sql(f"SELECT date, prcp FROM Measurement WHERE date >='{one_year_ago}' AND date <='{most_recent}'", conn)
    #print(precip_df)
    precip_json = precip_df.to_json(orient='records')   
    return (precip_json)
#%%
@app.route("/api/v1.0/stations")
def stations():
    conn = engine.connect()
    station_df = pd.read_sql("SELECT name, station FROM station",conn)
    station_json = station_df.to_json()
    return (station_json)


#%%

@app.route("/api/v1.0/tobs")
def tobs():
    conn = engine.connect()
    most_recent = pd.read_sql("SELECT date FROM measurement GROUP BY date ORDER BY date DESC LIMIT 1", conn)
    most_recent = most_recent['date'][0]
    one_year_ago = pd.read_sql(f"SELECT DATE('{most_recent}','-1 year') AS Date LIMIT 1", conn)
    one_year_ago = one_year_ago['Date'][0]
    tob_df = pd.read_sql(f"SELECT date, tobs AS temperature FROM measurement WHERE date >='{one_year_ago}' AND date <='{most_recent}'", conn)
    tob_json = tob_df.to_json(orient='records')
    return(tob_json)
#%%
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    conn = engine.connect()
    start_fix = start.replace("/", "-")
    end_fix = end.replace("/","-")
    temp_range = pd.read_sql(f"SELECT MIN(tobs) AS minimum_temperature, AVG(tobs) AS average_temperature, MAX(tobs) AS maximum_temperature FROM measurement WHERE date >='{start_fix}' AND date <='{end_fix}'", conn)
    temp_range_json = temp_range.to_json(orient='records')
    return(temp_range_json)
#%%

@app.route("/api/v1.0/<start>")
def start(start):
    conn = engine.connect()
    start_fix = start.replace("/", "-")
    temp_range = pd.read_sql(f"SELECT MIN(tobs) AS minimum_temperature, AVG(tobs) AS average_temperature, MAX(tobs) AS maximum_temperature FROM measurement WHERE date >='{start_fix}'", conn)
    temp_range_json = temp_range.to_json(orient='records')
    return(temp_range_json)
    

if __name__ == '__main__':
    app.run(debug=True)