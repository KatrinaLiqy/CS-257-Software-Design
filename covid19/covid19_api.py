#!/usr/bin/env python3
'''
    covid19_api.py
    Katrina Li, Lily Li, Wenlai Han
    Oct 16, 2020

    This program utlize a simple postgres database which stores all state info
    about COVID19 updates (new_deaths integer, new_positive_tests integer,
	new_negative_tests integer, new_hospitalizations integer) and a simple 
    API to give access to that database, and the API is implemented using 
    Flask and PostgreSQL.
    
    This program implements the following data flow:
        
        Client makes a request to Server, which makes a query of Database 'covid19', 
        which responds to Server, which responds to Client.
    
    We thought about object oriented programming strategy in implementing the API,
    but refrained to do so since it would only involve one single class. So we resolved to 
    utilize the convenience of a python program and connect to the database and 
    process part of the data globally in the program. We would transform our strategy
    to an oop one once we have a system of databases and items to keep in track all along.
'''
import sys
import argparse
import flask
import json
import psycopg2
import datetime

from config import database
from config import user
from config import password

app = flask.Flask(__name__)

try:
    connection = psycopg2.connect(
        database=database, user=user, password=password)
except Exception as e:
    print(e)
    exit()
try:
    cursor = connection.cursor()
    query = 'SELECT covid19_days.date,covid19_days.deaths,covid19_days.new_positive_tests,covid19_days.new_negative_tests,covid19_days.new_hospitalizations, covid19_days.state_id, states.abbreviation FROM covid19_days, states WHERE covid19_days.state_id = states.id;'
    cursor.execute(query)
except Exception as e:
    print(e)
    exit()

datalist = []
for row in cursor:
    datalist.append(row)


''' 
    Extract the state_abbreviation column from the datalist and creates a list of state_abbreviation
'''
state_abbreviation_list = []
for row in datalist:
    state_abbreviation_list.append(row[6])


def add_useful_daily_data(raw_datalist):
    '''
        Processes data from our database. After summing up COVID19 data in categories, it stores all the cumulative data as the values to the keys of the corresponding states in a dictionary. It returns all four relevant dictionaries in a list.

        Parameters:
        raw_datalist -- list that contains all the information after query

        Returns:
        useful_datalist -- list that contains four dictionaries which keys are state abbreviations and values are cumulative deaths/positive cases/negative cases/hospitalizations.
    '''
    cumulative_deaths = {}
    cumulative_positive = {}
    cumulative_negative = {}
    cumulative_hospitalizations = {}

    # Initialize the dictionary with all keys possible and default their values as 0
    for i in range(len(state_abbreviation_list)):
        cumulative_deaths[state_abbreviation_list[i]] = 0
        cumulative_positive[state_abbreviation_list[i]] = 0
        cumulative_negative[state_abbreviation_list[i]] = 0
        cumulative_hospitalizations[state_abbreviation_list[i]] = 0
    # Sum up the daily cases to a cumulative dataset and ignores the NULL items
    for row in raw_datalist:
        state_abbreviation = row[6]
        if row[1] != 'NULL' and row[1] != None:
            cumulative_deaths[state_abbreviation] += row[1]
        if row[2] != 'NULL':
            cumulative_positive[state_abbreviation] += row[2]
        if row[3] != 'NULL':
            cumulative_negative[state_abbreviation] += row[3]
        if row[4] != 'NULL':
            cumulative_hospitalizations[state_abbreviation] += row[4]
        else:
            continue

    useful_datalist = [cumulative_deaths, cumulative_positive,
                       cumulative_negative, cumulative_hospitalizations, raw_datalist[0][0]]
    return useful_datalist


@app.route('/state/<state_abbreviation>/daily')
def get_daily_state_data(state_abbreviation):
    ''' 
        For URL request of "/state/{state-abbreviation}/daily",
        this method gathers all relevant fields for the requested state
        from the user (start_date and end_date of the data avaliable, 
        the total number of deaths between the start and end dates, the
        number of positive and negative COVID-19 tests, and the number 
        of hospitalizations cases during that time range). Users can 
        only input the two-letter state_abbreviation in either lowercase
        or uppercase, but not the whole name.

        This methods returns a single JSON list of dictionaries representing all the daily statistics for the specified state.

        Parameters:
        state_abbreviation -- the string of two chars (like MN)

        Returns:
        json.dumps(state_data_list) -- dumps a list which includes a dictionary of a state's data
    '''
    state_data_list = []
    state_abbreviation_upper = state_abbreviation.upper()
    for row in datalist:
        if row[6] == state_abbreviation_upper:

            date_in_data = row[0]
            deaths_in_data = row[1]
            new_positive_in_data = row[2]
            new_negative_in_data = row[3]
            new_hospitalizations_in_data = row[4]
            state_abbrviation_in_data = row[6]

            daily_dictionary = {}
            daily_dictionary["date"] = date_in_data.strftime("%Y-%m-%d")
            daily_dictionary["state"] = state_abbrviation_in_data
            daily_dictionary["deaths"] = deaths_in_data
            daily_dictionary["positive"] = new_positive_in_data
            daily_dictionary["negative"] = new_negative_in_data
            daily_dictionary["hospitalizations"] = new_hospitalizations_in_data

            state_data_list.append(daily_dictionary)
            print(daily_dictionary)
    return json.dumps(state_data_list)


@app.route('/state/<state_abbreviation>/cumulative')
def get_cumulative_info(state_abbreviation):
    ''' 
        For URL request of "/state/{state-abbreviation}/cumulative",
        this method gathers all relevant fields for the requested state
        from the user (start_date and end_date of the data avaliable, 
        the total number of deaths between the start and end dates, the
        number of positive and negative COVID-19 tests, and the number 
        of hospitalizations cases during that time range). Users can 
        only input the two-letter state_abbreviation in either lowercase
        or uppercase, but not the whole name.

        This methods returns a single JSON dictionary representing the cumulative
        statistics for the specified state.

        Parameters:
        state_abbreviation -- the string of two chars (like MN)

        Returns:
        json.dumps(response_list) -- dumps a list which includes a dictionary of a state's cumulative data

    '''
    state_abbreviation = state_abbreviation.upper()
    raw_datalist = add_useful_daily_data(datalist)
    response = {}
    response["start_date"] = '2020-01-20'
    # convert end_date to a JSON serializable format
    response["end_date"] = raw_datalist[4].strftime("%Y-%m-%d")
    response["deaths"] = raw_datalist[0].get(state_abbreviation)
    response["positive"] = raw_datalist[1].get(state_abbreviation)
    response["negative"] = raw_datalist[2].get(state_abbreviation)
    response["hospitalizations"] = raw_datalist[3].get(state_abbreviation)
    response_list = [response]
    return json.dumps(response_list)


@app.route('/states/cumulative')
def get_sorted_cumulative_info():
    ''' 
        For URL request of "/states/cumulative?sort=[deaths|cases|hospitalizations]",
        this method gathers all relevant fields in the requested order
        of the user (start_date and end_date of the data avaliable, 
        the total number of deaths between the start and end dates, the
        number of positive COVID-19 tests, and the number 
        of hospitalizations cases during that time range). Users can 
        only select sorting criteriors from "deaths|cases|hospitalizations",
        with the default option being sorted by "deaths".

        This methods returns a single JSON list of dictionary representing the cumulative
        statistics for all states in the sorting order demanded.

        Returns:
        json.dumps(result) -- dumps a list of dictionaries that each contains a state's data, sorted in decreasing order either by deaths, positive cases or hospitalizations.
    '''
    sort_cumulative = {}
    indicator = flask.request.args.get('sort', default='deaths')

    useful_datalist = add_useful_daily_data(datalist)

    cumulative_deaths = useful_datalist[0]
    cumulative_positive = useful_datalist[1]
    cumulative_negative = useful_datalist[2]
    cumulative_hospitalizations = useful_datalist[3]
    latest_date = useful_datalist[4]

    result = []
    if (indicator == 'deaths'):
        sort_list = sorted(cumulative_deaths.items(),
                           key=lambda x: x[1], reverse=True)

    elif(indicator == 'cases'):
        sort_list = sorted(cumulative_positive.items(),
                           key=lambda x: x[1], reverse=True)

    elif(indicator == 'hospitalizations'):
        sort_list = sorted(cumulative_hospitalizations.items(),
                           key=lambda x: x[1], reverse=True)

    for i in sort_list:
        response = {}
        response["start_date"] = '2020-01-20'
        # convert end_date to a JSON serializable format
        response["end_date"] = latest_date.strftime("%Y-%m-%d")
        response["state"] = i[0]
        response["deaths"] = cumulative_deaths.get(i[0])
        response["positive"] = cumulative_positive.get(i[0])
        response["negative"] = cumulative_negative.get(i[0])
        response["hospitalizations"] = cumulative_hospitalizations.get(i[0])
        result.append(response)
    print(result)
    return json.dumps(result)


@app.route('/')
def welcome():
    return 'Welcome to the COVID19 Data API designed by Katrina, Lily, Wenlai! Please navigate yourself to other requests in corresponding URLs. You may start from \"/help\"  page to explore our URL options.'


@app.route('/help')
def get_help():
    '''
        Displays the help message

        Returns:
        help_message -- string of help message
    '''
    help_message = ''
    with flask.current_app.open_resource('static/help.html', 'r') as f:
        help_message = f.read()
    return help_message


if __name__ == '__main__':
    '''
        The main method uses argparse to read input from user about the 
        host on which this application is running and the port on which 
        this application is listening, and starts the server for our API.
    '''
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument(
        'host', help='the host on which this application is running')
    parser.add_argument(
        'port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)


connection.close()
