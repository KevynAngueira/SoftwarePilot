import os
import time
from geopy import distance
import pandas as pd
import requests
import json
#from datetime import time, timedelta

class AnafiSimulator:
	''' 
	Controller for simulated Parrot Anafi drone
	
	...
	
	Attributes
	----------
	drone : drone
		the drone object
	location : GPS coordinates
		the drone's current location
	starting_location: GPS coordinates
		the drone's starting location
	battery : drone battery level
		the drone's battery level	
	time: times mission length
		time takes to complete mission

	Methods
	-------
	start_mission()
		Establishes a connection with the drone and starts mission
	end_mission()
		Breaks current connection with the drone and stops mission
	get_starting_coordinates()
		Returns drone's starting gps coordinates
	fly_mission(starting_location, new_location)
		Flies drone to new location
	get_next_coordinate()
		Gets next GPS coordinates from API
	'''	
	
	def __init__(self):
		'''
		Parameters
		----------
		speed : speed
			speed of drone in miles per second
		
		battery_discharge_rate: battery discharge rate
			rate of battery discharge
		'''
		#self.location = (39.64389402777777, -82.81658444444443) #lat and long
		self.location = (0, 0)
		self.original_starting_location = (0, 0)
		self.battery_level = 1
		self.time = pd.Timestamp('2022-07-27T0:0:0.000000')
		print("time: ", self.time)
		print(type(self.time))
		#self.time = 0.0 # seconds

		# initialize pandas dataframe to store flight info
		column_names = ['datetime', 'start_location', 'end_location', 'flight_distance (ft)', 'battery %']
		self.data = pd.DataFrame(columns=column_names)
			
	def start_mission(self):
		print("mission started")
		#self.time = self.time + 0.083 # five seconds for setup
		self.time = self.time + pd.Timedelta(seconds=5)

		# get initial starting location from local csv
		self.original_starting_location = self.get_starting_coordinates()
		print("original starting location: ", self.original_starting_location)

		#write to df
		array = [self.time, self.original_starting_location, self.original_starting_location, 0, "{0:.0%}".format(self.battery_level)]
		self.data.loc[len(self.data)] = array

		# docker container sends photo corresponding to loc [x, y] and get back new location
		self.location = self.get_next_coordinates() #replace w/ API
		print("location: ", self.location)

		self.fly_mission(self.original_starting_location, self.location)

	def fly_mission(self, starting_location, location):
		# anafi flies 33 MPHr or 0.00916667 MPSec
		speed = 0.00916667
		battery_discharge_rate = 0.07 # calc this (33mph max 25 min)

		dist = distance.distance(starting_location, self.location).miles

		#self.time = self.time + dist*speed + 0.167 # 10 secs to hover, take pic, send pic, and recieve next location
		self.time = self.time + pd.Timedelta(seconds = (dist*speed + 10))# 10 secs to hover, take pic, send pic, and recieve next location

		self.battery_level = self.battery_level - dist*battery_discharge_rate - 0.01 # 1% battery decrease for each stop

		print("time: ", self.time)
		print("battery level: ", self.battery_level)

		#write to df, convert dist from miles to feet by mult by 5280
		array = [self.time, starting_location, self.location, round(dist*5280, 4), "{0:.0%}".format(self.battery_level)]
		self.data.loc[len(self.data)] = array

		# check time and battery level
		# end mission if time > 22 min (1320 sec) or battery < 20 %
		if ((self.battery_level <= 0.2) or (self.time.minute > 22)):
			self.end_mission(self.location, self.original_starting_location)

		starting_location = self.location #save current location as next starting location
		
		# call API to get new location
		# get new location from API
		self.location = self.get_next_coordinates() #replace w/ API
		print("next location: ", self.location)
		self.fly_mission(starting_location, self.location)
		
	def end_mission(self, location, starting_location):

		speed = 0.00916667
		battery_discharge_rate = 0.7 # calc this (33mph max 25 min)

		dist = distance.distance(self.location, self.original_starting_location).miles
		#self.time = self.time + dist*speed
		self.time = self.time + pd.Timedelta(seconds = (dist*speed))

		self.battery_level = self.battery_level - dist*battery_discharge_rate

		#write to df
		array = [self.time, self.location, starting_location, round(dist*5280, 4), "{0:.0%}".format(self.battery_level)]
		self.data.loc[len(self.data)] = array

		self.data.to_csv('output.csv', sep=',')

		print("mission ended")
		print("battery: ", self.battery_level)
		print("time: ", self.time)
		quit()


	def get_starting_coordinates(self):
		'''
		Returns the drone's starting gps coordinates
		
		Return
		----------
		coordinates : str[latitude, longitude]
			list containing the current latitude and longitude gps values
		'''

		header = ['photo_id', 'weight_pt', 'lat', 'long', 'alt']
		df = pd.read_csv("/home/jmkline/softwarepilot/SoftwarePilot/SoftwarePilotSimulator/data/cubePointers.csv", names=header)
		df.drop(df.tail(1).index,inplace=True) #drop last row
		df1 = df.sample()
		loc = (df1.iloc[0,2], df1.iloc[0,3])
		return loc
	

	def get_next_coordinates(self):
		'''
		Returns the drone's next gps coordinates to fly to
		
		Return
		----------
		coordinates : str[latitude, longitude]
			list containing the current latitude and longitude gps values
		'''

		# 1. w/ drone location, get corresponding photo from AC (from local directory)
		# 2. send photo and current location back to API
		# 3. recieve next location from API
		# 4. fly to next location
		# 5. repeat 

		# ip_address = "127.0.0.1"
		# port = 8000
		# url = "http://{}:{}/".format(ip_address, port)	

		# print("location: ", self.location)
		
		# #update this for current location
		# coordinates = {}
		# coordinates["latitude"] = str(self.location[0])
		# coordinates["longitude"] = str(self.location[1])
		# coordinates["altitude"] = "5"
		# #coordinates = {"latitude" : "39.64389425", "longitude" : "-82.81595972222222", "altitude" : "5"}
		# print("coordinates: ", coordinates)
		
		# response = requests.post(url= os.path.join(url,"getImage"), data = json.dumps(coordinates))
		# data = response.json()
		# print("data from api:", data)
		# coordinates = (data['latitude'], data['longitude'])
		# print("coordinates:", coordinates)
		# return coordinates

		header = ['photo_id', 'weight_pt', 'lat', 'long', 'alt']
		df = pd.read_csv("/home/jmkline/softwarepilot/SoftwarePilot/SoftwarePilotSimulator/data/cubePointers.csv", names=header)
		df.drop(df.tail(1).index,inplace=True) #drop last row
		df1 = df.sample()
		loc = (df1.iloc[0,2], df1.iloc[0,3])
		return loc



#drone.start_mission()
drone = AnafiSimulator()
drone.start_mission()
