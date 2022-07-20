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
