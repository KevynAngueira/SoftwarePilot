import docker

class SoftwarePilotDocker:
	'''
	docker wrapper library for easier interaction with SoftwarePilot
	
	...
	
	Attributes
	----------
	client : docker client
		the docker client
	
	Methods
	-------
	deploy_container(image, detach, ports)
		deploys a docker container from a given image and connects to it
	connect_to_container(container_id)
		connects to an active container
	run_command(container, command)
		runs a command on a given image
	list_containers()
		prints a list of all containers
	list_image()
		prints a list of all local images
	get_container_id(image_name)
		returns the short id of an active container from a given image name
	get_container_name(image_id)
		returns the image name of an active container from a given short id
	get_container_ip(image_id)
		returns the container ip of an active container from a given short id
	print_logs(container)
		prints the logs of an active container
	stop_container(container_id)
		stops an active container from a given container id
	stop_all_containers()
		stops all active containers
	'''
	
	def __init__(self):
		self.client = docker.from_env()
	
	def deploy_container(self, image, detach = True, ports = "None"):
		'''
		deploys a docker container from a given image and connects to it
		
		Parameters
		----------
		image : str
			the docker image to be run
		detach : bool, optional
			if True the docker is detached from the terminal (default = True)
		ports : map{ computer port : docker port }
			maps the ports from the docker to the machine
			
		Return
		----------
		container : Docker Container
			the deployed docker container
		'''
		
		try:
			container = self.client.containers.run(image, detach = detach, ports = ports)
		except:
			container = self.client.containers.run(image, detach = detach)
		print ("< Container deployed >")
		return container
	
	def connect_to_container(self, container_id):
		'''
		connects to an active container
		
		Parameters
		----------
		container_id : str
			the id of the container to connect to
			
		Return
		----------
		container : Docker Container 
			the connected docker container
		'''
		
		try:
			container = self.client.containers.get(container_id)
			print ("< Container {} connected >".format(container_id))
			return container
		except:
			print("Invalid container ID")

	def run_command(self, container, command):
		'''
		runs a command on a given image
		
		Parameters
		----------
		container : docker container
			the container to run the command on
		command : str
			the command to run
		'''
		
		container.exec_run(command)
		print ("< Command running >")
	
	def get_container_id(self, image_name):
		'''
		returns the short id of an active container from a given image name
		
		Parameters
		----------
		image_name : str
			the name of the image to fetch the short id of its container
			
		Return
		----------
		id : str
			the requested container short id
		'''
		
		for c in self.client.containers.list():
			container_image_name = c.image.tags[0].split(':')[0]
			if image_name == container_image_name:
				return c.short_id
		print("Container not found")
		return "None"
	
	def get_container_name(self, container_id):
		'''
		returns the image name of an active container from a given container short id
		
		Parameters
		----------
		container_id : str
			the id of the container to fetch the name of its image
		
		Return
		----------
		name : str
			the requested image name
		'''
		
		for c in self.client.containers.list():
			if container_id == c.id:
				image_name = c.image.tags[0].split(':')[0]
				return image_name
		print("Container not found")
		return "None"
		
	def get_container_ip(self, container_id):
		'''
		returns the ip address of an active container from a given short id
		
		Parameters
		----------
		container_id : str
			the id of the container to fetch the ip of
			
		Return
		----------
		ip : str
			the requested container ip
		'''
		
		api_client = docker.APIClient(base_url='unix://var/run/docker.sock')
		try:
			container_data = api_client.inspect_container(container_id)
			return container_data['NetworkSettings']['Networks']['bridge']['IPAddress']
		except:
			print ("Invalid container id")
				
	def print_logs(self, container):
		'''
		prints the logs of an active container
		
		Parameters
		----------
		container: docker container
			the container to print the logs of
		'''
		
		try:
			logs = container.logs(stream = True)
			while (True):
				try:
					print(next(logs, None))
				except:
					break
		except:
			print("Invalid container")
		
	def stop_container(self, container_id):
		'''
		stops an active container from a given container id
		
		Parameters
		----------
		container : docker container
			the container to stop
		
		'''
		
		try:
			container = connect_to_container(container_id)
			container.stop()
			print("< Container {} stopped >".format(container_id))
		except:
			print("Invalid container ID")
	
	def stop_all_containers(self):
		'''
		stops all active containers
		'''
	
		for container in self.client.containers.list():
  			container.stop()
  			
  	#Connect to a docker client on another machine  			
  	#List local images
  	#Add connect client off the machine given exposed port and IP
  	#When getting ID fix behavior with multiple instances
  

		
		
	
