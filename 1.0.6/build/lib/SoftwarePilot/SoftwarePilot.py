from SoftwarePilot.AnafiController import AnafiController
from SoftwarePilot.SoftwarePilotService import SoftwarePilotService
from SoftwarePilot.SoftwarePilotDocker import SoftwarePilotDocker
import socket

class SoftwarePilot:
	'''
	A library to control drones and services through python scripts
	
	...
	
	Attributes
	----------
	drone_dict : map{ str : DroneLibrary }
		the dictionary of supported drone types and their libraries
	drone : DroneLibrary
		the drone object
	docker : SoftwarePilotDocker
		docker wrapper library for easier interaction with SoftwarePilot
	service : SoftwarePilotService
		library to interact with the custom SoftwarePilot rest api service
		
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
		self.drone_dict = { "parrot_anafi": AnafiController }
	
	def setup_drone(self, drone_type, connection_method, download_dir):
		'''
		initiates and returns a drone object of the chosen drone type
		
		Parameters
		----------
		drone_type : DroneLibrary
			the drone type to be initiated
		connection_method : str
			the type of connection to be established to the drone
		download_dir : str
			the download path for drone media
			
		Return
		----------
		drone : DroneLibrary
			the drone object
		'''
		
		drone = self.drone_dict[drone_type](connection_method, download_dir)
		return drone
		
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
