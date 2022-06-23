from AnafiController import AnafiController

class SoftwarePilot:
	def __init__(self):
		self.drone_dict = { "parrot_anafi": AnafiController }
	
	def initialize_drone(self, drone_type, connection_method, download_dir):	
		return self.drone_dict[drone_type](connection_method, download_dir)
