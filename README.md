# SoftwarePilot
SoftwarePilot is an open source middleware and API that supports aerial applications. SoftwarePilot allows users to connect consumer Parrot Anafi drones to programmable pythonscripts that provide access to the drones flight controller, camera, and navigation system as well as custom rest api and dockerfile integration.

## Getting Started
### Install the library
1. Clone the repo, or
  ```sh
  git clone https://github.com/boredbot2/SoftwarePilot.git
  ```
2. Pip install
  ```sh
  pip install SoftwarePilot
  ```
### First Time Setup
Pair the drone:
```sh
1. Turn on the Parrot-Anafi drone.
2. Turn on the Skycontroller.
3. Connect a USB to USB-C cable to the controller and the drone respectively.
4. Wait until the blinking light on the controller turns into a solid blue light.
5. Disconnect the controller and the drone.
```	
Calibrate the drone:
```sh
1. Download the FreeFlight 6 app on your phone and perform all necesary authentication.
2. Connect a USB to USB-C cable to the controller and the phone.
3. Press Fly on the FreeFlight 6 app and follow the instructions on the screen.
4. Confirm calibration by launching and then landing the drone with the Up and Down arrows button on the controller.
5. Disconnect the controller and the phone.
```
### Setting Up
```sh
1. Turn on the Parrot-Anafi drone.
2. Turn on the Skycontroller.
3. Wait until the blinking light on the controller turns into a solid blue light.
	If the light does not turn solid blue, follow the Pair the drone instructions above.
4. Connect a USB to USB-C cable to the computer and the controller respectively.
5. Run the mission!
	If the drone does not takeoff when told, follow the Calibrate the drone instructions above.
```
## Demos
1. Simple Start:
  ```sh
	from SoftwarePilot import SoftwarePilot

	'''
	This is short demo demonstrating how to connect to the drone, and execute a few basic commands
	'''

	sp = SoftwarePilot()

	# Setup a parrot anafi drone, connected through a controller, without a specific download directory
	drone = sp.setup_drone("parrot_anafi", 1, "None")

	drone.connect()

	drone.piloting.takeoff()

	# The drone will move forward 10 meters (x, y, z, angle)
	drone.piloting.move_by(10,0,0,0, wait = True)

	drone.piloting.land()

	drone.disconnect()
  ```
2. Handling Media
  ```sh
	from SoftwarePilot import SoftwarePilot
	import time

	'''
	This is short demo demonstrating how to get drone media
	'''

	sp = SoftwarePilot()

	# Setup a parrot anafi drone, connected through a controller, without a specific download directory
	drone = sp.setup_drone("parrot_anafi", 1, "None")

	drone.connect()

	# Without a specified directory, media will be automatically downloaded to AnafiMedia/

	# Example of how to setup, take, and download photos
	drone.camera.media.setup_photo()
	drone.camera.media.take_photo()
	drone.camera.media.download_last_media()

	# Example of how to setup, take, and download recordings
	drone.camera.media.setup_recording()
	drone.camera.media.start_recording()
	time.sleep(5)
	drone.camera.media.stop_recording()
	drone.camera.media.download_last_media()

	# Example of how to setup and process video live feed
	drone.camera.media.setup_stream(
		yuv_frame_processing = "None", 
		yuv_frame_cb = "None",
		h264_frame_cb = "None",
		start_cb = "None",
		end_cb = "None",
		flush_cb = "None",
	)
	# All the callbacks are optional and are automatically set to "None"
	# When set to default the stream will download all the frames and provide framerate and bitrate metadata
	drone.camera.media.start_stream()
	time.sleep(5)
	drone.camera.media.stop_stream()

	drone.disconnect()
  ```
3. Service Interaction
  ```sh
	from SoftwarePilot import SoftwarePilot
	import time

	'''
	This is a short demo demonstrating how to boot up a dockerized service and requesting it with SoftwarePilot

	SoftwarePilot provides a python template of a Rest API which the user is meant to modify and dockerize
	This API is meant to offload the image processing workload to a more capable machine
	SoftwarePilot does not limit the service to which it will connect to, but the basic structure must be followed for proper behavior
	'''

	sp = SoftwarePilot()

	sp.setup_docker()
	time.sleep(5)

	# REPLACE : DOCKER_IMAGE
	container = sp.docker.deploy_container("DOCKER_IMAGE", detach = True, ports = {8000:8000})

	ip_host = sp.get_host_ip()
	service = sp.setup_service(ip_address = ip_host)
	response = service.get()
	print(response)

	# REPLACE : IMAGE_PATH
	response = service.run("IMAGE_PATH")
	print(response)
  ```
4. All Together
  ```sh
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
  ```
## Authors
* **[Kevyn Angueira Irizarry](https://github.com/boredbot2)**

# Acknowledgements
*This work has been funded by grants from the National Science Foundation, including the ICICLE AI Institute (OAC 2112606)*
