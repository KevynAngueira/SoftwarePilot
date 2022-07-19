from SoftwarePilot import SoftwarePilot
import time

'''
This is a short demos of most of the utilities provided by SoftwarePilot

Make sure to build a custom docker image using the SoftwarePilotAPI.py as a template
'''

sp = SoftwarePilot()
sp.setup_docker()



drone = sp.setup_drone("parrot_anafi", 1, "None")
drone.connect()

drone.camera.media.setup_photo()
drone.piloting.takeoff()

num_img = 0
while (num_img < 5):
	drone.camera.media.take_photo()
	image_path = drone.camera.media.download_last_media()
	
	num_img += 1

drone.piloting.land()	

drone.disconnect()
