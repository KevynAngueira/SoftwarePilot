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
