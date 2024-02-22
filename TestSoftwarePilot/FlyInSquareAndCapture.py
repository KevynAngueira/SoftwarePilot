from SoftwarePilot import SoftwarePilot
import time

sp = SoftwarePilot()

# Output hello
print("Hello World!")

# Setup a parrot anafi drone, connected through a controller, without a specific download directory
drone = sp.setup_drone("parrot_anafi", 1, "None")

drone.connect()

# Set up photo
drone.camera.media.setup_photo()

drone.piloting.takeoff()

# The drone will move forward 10 feet (x, y, z, angle)
drone.piloting.move_by(10,0,0,0)

# Take a picture
drone.camera.media.take_photo()
drone.camera.media.download_last_media()

# Take a pause
time.sleep(10)

# The drone will rotate 90 degrees
drone.piloting.move_by(0,0,0,90)
# The drone will move forward 10 feet (x, y, z, angle)
drone.piloting.move_by(10,0,0,0)

# Take a picture
drone.camera.media.take_photo()
drone.camera.media.download_last_media()

# Take a pause
time.sleep(10)

# The drone will rotate 90 degrees
drone.piloting.move_by(0,0,0,90)
# The drone will move forward 10 feet (x, y, z, angle)
drone.piloting.move_by(10,0,0,0)

# Take a picture
drone.camera.media.take_photo()
drone.camera.media.download_last_media()

# Take a pause
time.sleep(10)

# The drone will rotate 90 degrees
drone.piloting.move_by(0,0,0,90)
# The drone will move forward 10 feet (x, y, z, angle)
drone.piloting.move_by(10,0,0,0)

# Take a picture
drone.camera.media.take_photo()
drone.camera.media.download_last_media()

# Take a pause
time.sleep(10)

drone.piloting.land()

drone.disconnect()
