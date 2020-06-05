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
    one_year_ago = pd.read_sql(f"SELECT DATE('{most_recent}','-1 year') AS Date LIMIT 1", conn)
    one_year_ago = one_year_ago['Date'][0]
    precip_df = pd.read_sql(f"SELECT date, prcp FROM Measurement WHERE date >='{one_year_ago}' AND date <='{most_recent}' ORDER BY date", conn)
    ### Putting the results into a dictionary where date is the key and prcp is value
    precip_dict = {}
    for index, row in precip_df.iterrows():
        precip_dict[row[0]]=[row[1]]
    precip_df = pd.DataFrame(precip_dict)
    precip_json = precip_df.to_json(orient = 'records')   
    return (precip_json)
#%%
@app.route("/api/v1.0/stations")
def stations():
    conn = engine.connect()
    station_df = pd.read_sql("SELECT name, station FROM station",conn)
    ##turning results into a list of stations
    stations_list = []
    for index, row in station_df.iterrows():
        stations_list.append(row[0])
    return jsonify(stations_list)


#%%

@app.route("/api/v1.0/tobs")
def tobs():
    conn = engine.connect()
    most_recent = pd.read_sql("SELECT date FROM measurement GROUP BY date ORDER BY date DESC LIMIT 1", conn)
    most_recent = most_recent['date'][0]
    one_year_ago = pd.read_sql(f"SELECT DATE('{most_recent}','-1 year') AS Date LIMIT 1", conn)
    one_year_ago = one_year_ago['Date'][0]
    tob_df = pd.read_sql(f"SELECT date, tobs AS temperature FROM measurement WHERE date >='{one_year_ago}' AND date <='{most_recent}'", conn)
    #tob_json = tob_df.to_json(orient='records')
    #Creating just a list of temperatures
    tobs_list = []
    for index,row in tob_df.iterrows():
        tobs_list.append(row[1])
    return jsonify(tobs_list)
#%%
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    conn = engine.connect()
    start_fix = start.replace("/", "-")
    end_fix = end.replace("/","-")
    temp_range = pd.read_sql(f"SELECT MIN(tobs) AS minimum_temperature, AVG(tobs) AS average_temperature, MAX(tobs) AS maximum_temperature FROM measurement WHERE date >='{start_fix}' AND date <='{end_fix}'", conn)
    #temp_range_json = temp_range.to_json(orient='records')
    #Creating a lits of the three temp info
    start_end_list = []
    for index,row in temp_range.iterrows():
        start_end_list.append(row[0])
        start_end_list.append(row[1])
        start_end_list.append(row[2])
    return jsonify(start_end_list)
#%%

@app.route("/api/v1.0/<start>")
def start(start):
    conn = engine.connect()
    start_fix = start.replace("/", "-")
    temp_ranges = pd.read_sql(f"SELECT MIN(tobs) AS minimum_temperature, AVG(tobs) AS average_temperature, MAX(tobs) AS maximum_temperature FROM measurement WHERE date >='{start_fix}'", conn)
    #temp_range_json = temp_range.to_json(orient='records')
    #Creating a list of the three temp info
    start_list = []
    for index,row in temp_ranges.iterrows():
        start_list.append(row[0])
        start_list.append(row[1])
        start_list.append(row[2])
    return jsonify(start_list)
    

if __name__ == '__main__':
    app.run(debug=True)