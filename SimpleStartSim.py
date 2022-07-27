from SoftwarePilot import SoftwarePilot

'''
This is short demo demonstrating how to connect to the drone, and execute a few basic commands
'''

sp = SoftwarePilot()

# Setup a parrot anafi drone, connected through a controller, without a specific download directory
drone = sp.setup_drone("parrot_anafi_simulator", "physical")

drone.start_mission()


