from SoftwarePilot import SoftwarePilot
from pynput import keyboard
sp = SoftwarePilot()

# Setup a parrot anafi drone, connected through a controller, without a specific download directory
drone = sp.setup_drone("parrot_anafi", 1, "None")
drone.connect()

drone.piloting.takeoff()

while(True):
	action = input()
	if (action == "w"):
		print("up")
		drone.piloting.move_by(1, 0, 0, 0, wait=False)
	if (action == "s"):
		print("down")
		drone.piloting.move_by(-1, 0, 0, 0, wait=False)
	if (action == "a"):
		print("left")
		drone.piloting.move_by(0, 1, 0, 0, wait=False)
	if (action == "d"):
		print("right")
		drone.piloting.move_by(0, -1, 0, 0, wait=False)

# drone.piloting.land()
#
# drone.disconnect()
