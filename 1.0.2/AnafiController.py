import os
import olympe
from AnafiCamera import AnafiCamera
from AnafiPiloting import AnafiPiloting
from AnafiRTH import AnafiRTH
from olympe.messages.ardrone3.PilotingState import PositionChanged

class AnafiController:
	def __init__(self, connection_type = 1, download_dir = "None"):
		if connection_type == "physical" or connection_type == 0:
			self.drone_ip = "192.168.42.1"		
			self.drone_rtsp_port = os.environ.get("DRONE_RTSP_PORT")
			self.drone_url = "http://{}/".format(self.drone_ip)

		elif connection_type == "controller" or connection_type == 1:
			self.drone_ip = "192.168.53.1"		
			self.drone_rtsp_port = os.environ.get("DRONE_RTSP_PORT", "554")
			self.drone_url = "http://{}:180/".format(self.drone_ip)
		else:
			raise RuntimeError("Illegal object parameter")

		self.drone = olympe.Drone(self.drone_ip)
		if download_dir == "None":
			if os.path.isdir("AnafiMedia") == False:			
				os.mkdir("AnafiMedia")			
			self.download_dir = "AnafiMedia"
		else:
			if os.path.isdir(download_dir) == False:
				os.mkdir(download_dir)
			self.download_dir = download_dir

		self.camera = AnafiCamera(self.drone, self.drone_ip, self.drone_rtsp_port, self.drone_url, self.download_dir)
		self.piloting = AnafiPiloting(self.drone)
		self.rth = AnafiRTH(self.drone)
		self.rth.setup_rth()
			
	def connect(self):
		assert self.drone.connect(retry = 3)
		print("< Drone Connected >")
	
	def disconnect(self):
		assert self.drone.disconnect()
		print("< Drone Disconnected >")
	
	def get_drone_coordinates(self):
		print ("Latitude: ", self.drone.get_state(PositionChanged)["latitude"])
		print ("Longitude: ", self.drone.get_state(PositionChanged)["longitude"])
		print ("Altitude: ", self.drone.get_state(PositionChanged)["altitude"])
