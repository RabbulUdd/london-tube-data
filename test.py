# Given tube station, create all the tube line passing through that station
# Given a tube line name print all the station names on that line

# SQL

import json


# # remember to change this
# # ------------------------------------------------------------------------------
# with open('d:\\vaticleint\\london-tube-data\\train-network.json') as file:
#     data = json.load(file)
#     # print(data[0])

#     # for i in data['stations']:
#     #     print(i)

#     for i in data['lines']:
#         print(i)

# ----------------------------------------

import psycopg2


def loadData():
	# connection establishment
	conn = psycopg2.connect(
	database="postgres",
		user='postgres',
		password='password',
		host='localhost',
		port= '5432'
	)

	conn.autocommit = True

	# Creating a cursor object
	cursor = conn.cursor()

	# query to create a database
	
	sql = ''' DROP TABLE lines'''
	cursor.execute(sql)

	sql = ''' DROP TABLE stations'''
	cursor.execute(sql)
	

	# sql = ''' CREATE database TubeNetwork '''
	# cursor.execute(sql)

	sql = ''' CREATE TABLE stations (
		name VARCHAR ( 50 ) NOT NULL,
		id VARCHAR(15) UNIQUE NOT NULL PRIMARY KEY,
		longitude NUMERIC NOT NULL,
		latitude NUMERIC NOT NULL
	) '''
	cursor.execute(sql)

	data = importJsonData()

	for station in data["stations"]:
		name = "{}".format(station["name"]).replace("'","\\''")
		id = "{}".format(station["id"])
		longitude = station["longitude"]
		latitude = station["latitude"]

		sql = ''' INSERT INTO stations (name, id, longitude, latitude)
		VALUES ('{}', '{}', {}, {}) '''.format(name, id, longitude, latitude)

		cursor.execute(sql)


	sql = ''' CREATE TABLE lines (
		name VARCHAR ( 50 ) NOT NULL,
		stationID VARCHAR(15) REFERENCES stations (id)
	) '''
	cursor.execute(sql)


	for line in data["lines"]:
		name = line["name"]
		stations = line["stations"]

		print(name)

		for station in stations:
			sql = ''' INSERT INTO lines (name, stationID) VALUES('{}', '{}')'''.format(name, station)
			cursor.execute(sql)

	# sql = "SELECT * FROM stations"
	# cursor.execute(sql)



	# Closing the connection
	conn.close()

def importJsonData():
	with open('train-network.json') as file:
		data = json.load(file)
		
		return data

def cli():
	programEnd = False
	while not programEnd:
		print("1. Would you like to find the lines passing through a station?")
		print("2. Would you like to find the stations in a line?")
		print("3. Would you like to end the program?")
		print()

		name = input("Please press 1,2 or 3? ")

		validInput = ["1", "2", "3"]

		if input not in validInput:
			print("Please Enter A valid input with")


		programEnd = True


# cli()

loadData()