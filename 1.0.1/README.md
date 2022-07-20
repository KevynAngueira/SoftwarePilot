# SoftwarePilot
SoftwarePilot is an open source middleware and API that supports aerial applications. SoftwarePilot allows users to connect consumer Parrot Anafi drones to programmable pythonscripts that provide access to the drones flight controller, camera, and navigation system as well as custom rest api and dockerfile integration.

## Getting Started
Install the library:
1. Clone the repo
  ```sh
  git clone https://github.com/boredbot2/SoftwarePilot.git
  ```
2. Pip install
  ```sh
  pip install SoftwarePilot
  ```
## Examples
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

	# The drone will move forward 10 feet (x, y, z, angle)
	drone.piloting.move_by(10,0,0,0)

	drone.piloting.land()

	drone.disconnect()
  ```

## Authors
* **[Kevyn Angueira Irizarry](https://github.com/boredbot2)**

