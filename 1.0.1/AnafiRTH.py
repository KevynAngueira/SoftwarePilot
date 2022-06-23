import olympe
from olympe.messages.rth import ( 
	set_preferred_home_type,
	set_custom_location,
	set_auto_trigger_mode,
	set_delay,
	set_ending_behavior,
	set_ending_hovering_altitude,
	return_to_home,
	abort,
	cancel_auto_trigger,
)

class AnafiRTH:
	def __init__(self, drone_object):
		self.drone = drone_object
	
	'''
	Sets up the return to home:
	
	home_type - takeoff/pilot/custom
	gps_coordinates - longitude,latitude,altitude (comma sepparated string) *only used it home_type is custom
	auto_trigger - on/off (automatically flies back in case of disconnection or low battery)
	delay - delay in seconds before auto_trigger RTH in case of disconnection
	ending_behavior - landing/hovering (behavior after reaching home)
	ending_hovering_altitude - meters from ground leve to hover at after reaching home *only used when ending_behavior is hovering
	'''	
	def setup_rth(self, 
		home_type = "takeoff",
		gps_coordinates = "None",
		auto_trigger = "on",
		delay = 5,
		ending_behavior = "landing",
		ending_hovering_altitude = 2
	):
		self.drone(set_preferred_home_type(home_type)).wait()
		if home_type == "custom":
			gps_coordinates = gps_coordinates.split(',')
			self.drone(set_custom_location(gps_coordinates[0], gps_coordinates[1], gps_coordinates[2])).wait()
		self.drone(set_auto_trigger_mode(auto_trigger)).wait()
		self.drone(set_delay(delay)).wait()
		self.drone(set_ending_behavior(ending_behavior)).wait()
		if ending_behavior == "hovering":
			self.drone(set_ending_hovering_altitude(ending_hovering_altitude)).wait()

	def return_to_home(self):
		self.drone(return_to_home()).wait()

	def abort_return_to_home(self):
		self.drone(abort()).wait()

	def cancel_auto_trigger(self):
		self.drone(cancel_auto_trigger).wait()
