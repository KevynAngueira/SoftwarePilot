from SoftwarePilot import SoftwarePilot
import time

'''
This is a short demo combining all the utilies demonstrated
'''

sp = SoftwarePilot()

sp.setup_docker()
time.sleep(5)
# Dockerize SoftwarePilotAPITest and replace "DOCKER_IMAGE" for your custom name
container = sp.docker.deploy_container("DOCKER_IMAGE", detach = True, ports = {8000:8000})

ip_host = sp.get_host_ip()
service = sp.setup_service(ip_address = ip_host)

response = service.get()
print(response)

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

