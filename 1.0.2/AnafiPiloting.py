import olympe
from olympe.messages.ardrone3.Piloting import (
	TakeOff,
	Landing,
	moveBy,
	moveTo,
	CancelMoveTo,
	CancelMoveBy,
)
from olympe.messages.ardrone3.PilotingState import (
	FlyingStateChanged,
	PositionChanged,
	moveToChanged,	
)

# << Drone Flight Methods >>
class AnafiPiloting:
	def __init__(self, drone_object):
		self.drone = drone_object	

	def takeoff(self):
		assert self.drone(
			TakeOff()
			>> FlyingStateChanged(state = "hovering", _timeout=5)
		).wait().success()
	
	def land(self):
		assert self.drone(Landing()).wait().success()

	'''		
	Moves the drone a specified number of meters and changes its orientation relative to its current heading:

	x - forward and backwards (meters)
	y - left and right (meters)
	z - up and down (meters)
	angle - radians (radians)
	'''
	def move_by(self, x, y, z, angle):
		assert self.drone(
			moveBy(x, y, z, angle)
			>> FlyingStateChanged(state = "hovering", _timeout=5)
		).wait().success()
	
	'''
	Moves the drone to a specified waypoint given given in gps coordinates:

	latitude - left and right relative to north
	longitude - forward and backwards relative to north
	altitude - up and down relative to the floor (meters)
	orientation_mode - NONE/heading_start/heading_during
	heading - radians relative to north *Only applicable when orientation_mode is not NONE
	'''
	def move_to(self, lat, lon, alt, orientation_mode = "NONE", heading = 0):
		assert self.drone(
			moveTo(
				latitude = lat,
				longitude = lon,
				altitude = alt,
				orientation_mode = orientation_mode,
				heading = heading,
			)
			>> moveToChanged(status = "DONE")
		).wait().success()
		
	def cancel_move_by(self):
		self.drone.CanceMoveBy()

	def cancel_move_to(self):
		self.drone.CancelMoveTo()
