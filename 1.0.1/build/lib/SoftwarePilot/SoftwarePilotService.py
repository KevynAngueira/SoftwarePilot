import requests
import json

class SoftwarePilotService:
	'''
	library to interact with the custom SoftwarePilot rest api service
	
	...
	
	Attributes
	----------
	ip_address : str
		the ip address to request the rest api
	port : int
		the port used to request the rest api
	url : str
		the url used to request the rest api
	
	Methods
	-------
	set_service(ip_address, port)
		initializes the variables needed to request the rest api
	get(extension)
		executes a get request to the service
	get_ip_address()
		returns the ip address to request the rest api
	get_port()
		returns the port to request the rest api
	get_input_shape()
		returns the input shape expected by the rest api
	get_output_keys()
		returns the output keys returned by the rest api
	get_download_path()
		returns the download path where images would be uploaded
	run(image)
		executes a post request to the service, including an image file and returning a json of shape output_keys
	'''
	
	def __init__(self, ip_address, port):
		'''
		Parameters
		----------
		ip_address : str
			the ip address to request the rest api
		port: str
			the port used to request the rest api
		'''
		
		self.set_service(ip_address, port)
	
	def set_service(self, ip_address, port):
		'''
		initializes the variables needed to request the rest api
		
		Parameters
		----------
		ip_address : str
			the ip address to request the rest api
		port: str
			the port used to request the rest api
		'''
		
		self.ip_address = ip_address
		self.port = port
		self.url = "http://{}:{}/".format(self.ip_address, self.port)

	def get(self, extension = ""):
		'''
		executes a get request to the service
		
		Parameters
		----------
		extension : str, optional
			parameter to make a get request to a specific extension (default = "")
			
		Return
		----------
		data : json
			the get response
		'''
		
		response = requests.get(url = (self.url+extension))
		data = response.json()
		return data

	def get_ip_address(self):
		'''
		returns the ip address to request the rest api
		
		Return
		----------
		ip_address : str
			the ip_address
		'''
		
		return self.ip_address
	
	def get_port(self):
		'''
		returns the port to request the rest api
		
		Return
		----------
		port : int
			the port
		'''
		
		return self.port
	
	def get_input_shape(self):
		'''
		returns the input shape expected by the rest api
		
		Return
		----------
		data : int[]
			the input shape
		'''
		
		data = self.get()	
		return data["input shape"]
	
	def get_output_keys(self):
		'''
		returns the output keys returned by the rest api
		
		Return
		----------
		output_keys : str[]
			the output keys
		'''
		
		data = self.get()	
		return data["output keys"]
	
	def get_download_path(self):
		'''
		returns the download path where images would be uploaded
		
		Return
		----------
		download_path : str
			the image download path
		'''
		
		data = self.get()
		return data["download path"]
	
	def run(self, image_path):
		'''
		executes a post request to the service, including an image file and returning a json of shape output_keys
		
		Parameters
		----------
		image_path : str
			path to the image to upload
		
		Return
		----------
		data : any[]
			the image post response
		'''
		
		extension = "image/"
		file = {'file': open(image_path, 'rb')}
		response = requests.post(url=(self.url+extension), files=file)
		data = response.json()
		return data
