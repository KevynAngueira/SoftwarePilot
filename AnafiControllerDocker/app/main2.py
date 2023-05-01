import time
from AnafiController import AnafiController

drone = AnafiController()
drone.connect()

drone.piloting.takeoff()
time.sleep(5)
drone.piloting.land()

drone.disconnect()
