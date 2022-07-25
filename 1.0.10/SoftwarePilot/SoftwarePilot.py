from SoftwarePilot.SoftwarePilotService import SoftwarePilotService
from SoftwarePilot.SoftwarePilotDocker import SoftwarePilotDocker
import socket
import importlib

class SoftwarePilot:
	'''
	A library to control drones and services through python scripts
	
	...
	
	Attributes
	----------
	drone_lib_dict : map{str:str}
		a map of all integrated drone libraries
	docker : SoftwarePilotDocker
		docker wrapper library for easier interaction with SoftwarePilot
	
	Methods
	-------
	setup_drone(drone_type, connection_method, download_dir)
		initiates and returns a drone object of the chosen drone type
	setup_docker()
		iniates a docker client
	setup_service(ip_adress, port)
		initiates and returns a SoftwarePilotService object that connects to the given web api
	get_host_ip()
		gets the host's ip address
	'''
	def __init__(self):
		self.drone_lib_dict = {"parrot_anafi" : "AnafiController"}
	
	def setup_drone(self, drone_type, connection_method, download_dir="None"):
		'''
		initiates and returns a drone object of the chosen drone type
		
		Parameters
		----------
		drone_type : DroneLibrary
			the drone type to be initiated
		connection_method : str
			the type of connection to be established to the drone
		download_dir : str, optional
			the download path for drone media (default = "None")
			
		Return
		----------
		drone : DroneLibrary
			the drone object
		'''
		
		try:
			if drone_type in self.drone_lib_dict.keys():
				drone_type = self.drone_lib_dict[drone_type]
				drone_lib = importlib.import_module("SoftwarePilot." + drone_type)
			else:	
				drone_lib = importlib.import_module(drone_type)
			drone_call = getattr(drone_lib, drone_type)
			drone = drone_call(connection_method, download_dir="None")
			return drone
		except:
			print (f"ModuleError: Invalid drone module '{drone_type}'")
			return None
	
	def setup_docker(self):
		'''
		iniates a docker client
		'''
		
		self.docker = SoftwarePilotDocker()
		
	def setup_service(self, ip_address = "172.0.0.1", port = 8000):
		'''
		initiates and returns a SoftwarePilotService object that connects to the given web api
		
		Parameters
		----------
		ip_address : str, optional
			the ip address to be used for the web api requests (default = "172.0.0.1")
		port : int, optional
			the port to be used for the web api requests (default = 8000)
		
		Return
		----------
		service : SoftwarePilotService
			the service object meant to interact with the rest api
		'''
		
		service = SoftwarePilotService(ip_address = ip_address, port = port)
		return service

	def get_host_ip(self):
		'''
		gets the host's ip address
		
		Return
		----------
		ip_address : str
			the host's ip address
		'''
		
		hostname = socket.gethostname()   
		ip_address = socket.gethostbyname(hostname)
		return ip_address
