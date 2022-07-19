from SoftwarePilot import SoftwarePilot
import time

'''
This is a short demos of most of the utilities provided by SoftwarePilot

Make sure to build a custom docker image using the SoftwarePilotAPI.py as a template
'''


sp = SoftwarePilot()
sp.setup_docker()

# REPLACE : Docker image name
container = sp.docker.deploy_container("CUSTOM_DOCKER_IMAGE", detach = True, ports = {8000:8000})

time.sleep(5)

ip_host = sp.get_host_ip()
service = sp.setup_service(ip_address = ip_host)
service.get()

download_dir = service.get_download_path()
drone = sp.setup_drone("parrot_anafi", 1, download_dir)
drone.connect()

drone.camera.media.setup_photo()
drone.piloting.takeoff()

num_img = 0
while (num_img < 20):
	drone.camera.media.take_photo()
	image_path = drone.camera.media.download_last_media()
	
	response = service.run(image_path)
	print(response)
	drone.piloting.move_by(response['x'], response['y'], response['z'], response['angle'])
	
	num_img += 1

drone.piloting.land()	

drone.disconnect()
