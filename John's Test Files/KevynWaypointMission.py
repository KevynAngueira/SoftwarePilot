''' 
Given a CSV file containing waypoint data,this Code implements a Wapoint mission on an anafi parrot sUAV. The code is adapted from a sample
program written by Kevyn Angueira.

'''

# from SoftwarePilot import SoftwarePilot
import sys
import csv
import time


def getWaypointFiles():
    return sys.argv[1:]


class WaypointTraverser:
	def __init__(self):
		self.filename = ""
		self.waypoint_num = 0

	# actionType = -1
	def noAction(self, drone, param):
	    pass

	# actionType = 0
	def pauseDrone(self, drone, param):
	    time.sleep(param/1000.0)

	# actionType = 1
	def takePhoto(self, drone, param):
	    drone.camera.media.take_photo()
	    drone.camera.media.download_last_media(name = (self.filename + "_" + self.waypoint_num))

	# actionType = 5
	def tiltGimbal(self, drone, param):
	    drone.camera.controls.reset_alignment_offset()
	    drone.camera.controls.set_alignment_offset(0, param, 0)

	def executeAction(self, drone, action, param):
	    action_map = {-1: self.noAction, 0: self.pauseDrone, 1: self.takePhoto, 5: self.tiltGimbal}
	    action_map[action](drone, param)

	def traverseWaypointFile(self, filename, drone):   
		self.filename = filename[:-3]
		with open(filename, 'r') as waypoint_file:
			# Creating a csv reader for the waypoint file
			waypoint_reader = csv.reader(waypoint_file)
			fields = next(waypoint_reader)

			self.waypoint_num = 0
			for waypoint in waypoint_reader:            
				latitude = float(waypoint[0])
				longitude = float(waypoint[1])
				'''
				Unsure if altitude is measured in meters or in feet
				Use top one if its in feet
				'''
				# altitude = waypoint[2]
				altitude = float(waypoint[2])/3.28084
				heading = float(waypoint[3])

				drone.piloting.move_to(latitude, longitude, altitude, heading=heading)
				'''
				print(latitude)
				print(longitude)
				print(altitude)
				print(heading)
				'''
	
				for x in range(8, 37, 2):
					action = int(waypoint[x])
					self.executeAction(drone, action, action+1)
					print(action)
					if (action == -1):
						break
				self.waypoint_num += 1


if __name__ == "__main__":
	'''
	Unsure if altitude is measured in meters or in feet
	Use top one if its in feet
	'''
	traverser = WaypointTraverser()

	# CLEARANCE_ALTITUDE = 10
	CLEARANCE_ALTITUDE = 3

	waypoint_files = getWaypointFiles()
	
	sp = SoftwarePilot()
	drone = sp.setup_drone("parrot_anafi", 1, "None")
	drone.connect()

	home = drone.get_drone_coordinates()
	drone.camera.media.setup_photo()
	drone.piloting.takeoff()
	
	for filename in waypoint_files:
		traverser.traverseWaypointFile(filename, drone)
	
	drone.piloting.move_to(home[0], home[1], CLEARANCE_ALTITUDE)
	drone.piloting.land()

	drone.disconnect()
