from AnafiCameraMedia import AnafiCameraMedia
from AnafiCameraControls import AnafiCameraControls

class AnafiCamera:
	def __init__(self, drone_object, drone_ip, drone_rtsp_port, drone_url, download_dir):
		self.media = AnafiCameraMedia(drone_object, drone_ip, drone_rtsp_port, drone_url, download_dir)
		self.controls = AnafiCameraControls(drone_object)
