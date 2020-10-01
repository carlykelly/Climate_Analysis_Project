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
        f"Welcome! Please enter date as yyyy-mm-dd<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startdate/enddate<br/>"
    )
#%%
@app.route("/api/v1.0/precipitation")
def precipitation():
    conn = engine.connect()
    most_recent = pd.read_sql("SELECT date FROM measurement GROUP BY date ORDER BY date DESC LIMIT 1", conn)
    most_recent = most_recent['date'][0]
    one_year_ago = pd.read_sql(f"SELECT DATE('{most_recent}','-1 year') AS Date LIMIT 1", conn)
    one_year_ago = one_year_ago['Date'][0]
    precip_df = pd.read_sql(f"SELECT date, prcp FROM Measurement WHERE date >='{one_year_ago}' AND date <='{most_recent}' ORDER BY date", conn)
    precip_df = precip_df.groupby('date').mean()
    return pd.Series(precip_df['prcp'],precip_df.index).to_json()

#%%
@app.route("/api/v1.0/stations")
def stations():
    conn = engine.connect()
    station_df = pd.read_sql("SELECT name, station FROM station",conn)
    station_list = list(station_df['name'])
    return jsonify(station_list)

#%%

@app.route("/api/v1.0/tobs")
def tobs():
    conn = engine.connect()
    most_recent = pd.read_sql("SELECT date FROM measurement GROUP BY date ORDER BY date DESC LIMIT 1", conn)
    most_recent = most_recent['date'][0]
    one_year_ago = pd.read_sql(f"SELECT DATE('{most_recent}','-1 year') AS Date LIMIT 1", conn)
    one_year_ago = one_year_ago['Date'][0]
    tob_df = pd.read_sql(f"SELECT date, tobs AS temperature FROM measurement WHERE date >='{one_year_ago}' AND date <='{most_recent}'", conn)
    tob_list = list(tob_df['temperature'])
    return jsonify(tob_list)
#%%
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    conn = engine.connect()
    start_fix = start.replace("/", "-")
    end_fix = end.replace("/","-")
    temp_range = pd.read_sql(f"SELECT MIN(tobs) AS minimum_temperature, AVG(tobs) AS average_temperature, MAX(tobs) AS maximum_temperature FROM measurement WHERE date >='{start_fix}' AND date <='{end_fix}'", conn)
    start_end_list = []
    start_end_list.append(temp_range['minimum_temperature'][0])
    start_end_list.append(temp_range['average_temperature'][0])
    start_end_list.append(temp_range['maximum_temperature'][0])
    return jsonify(start_end_list)
#%%

@app.route("/api/v1.0/<start>")
def start(start):
    conn = engine.connect()
    start_fix = start.replace("/", "-")
    temp_ranges = pd.read_sql(f"SELECT MIN(tobs) AS minimum_temperature, AVG(tobs) AS average_temperature, MAX(tobs) AS maximum_temperature FROM measurement WHERE date >='{start_fix}'", conn)
    start_list = []
    start_list.append(temp_ranges['minimum_temperature'][0])
    start_list.append(temp_ranges['average_temperature'][0])
    start_list.append(temp_ranges['maximum_temperature'][0])
    return jsonify(start_list)

if __name__ == '__main__':
    app.run(debug=True)