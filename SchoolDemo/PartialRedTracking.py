import cv2
import numpy as np
import math
import time
import queue
import olympe
from SoftwarePilot import SoftwarePilot

LENGTH_ANGLE = 75
WIDTH_ANGLE = 30




class RedTracker:
	def __init__(self, drone):
		self.drone = drone
		self.media = drone.camera.media
		
	def boundRed(self, cv2img):
		image = cv2img
		img_shape = image.shape[:-1]
		
		result = image.copy()
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		# lower boundary RED color range values; Hue (0 - 10)
		lower1 = np.array([0, 100, 20])
		upper1 = np.array([10, 255, 255])

		# upper boundary RED color range values; Hue (160 - 180)
		lower2 = np.array([160, 100, 20])
		upper2 = np.array([179, 255, 255])
		
		lower_mask = cv2.inRange(image, lower1, upper1)
		upper_mask = cv2.inRange(image, lower2, upper2)
		
		full_mask = lower_mask + upper_mask;
		result = cv2.bitwise_and(result, result, mask=full_mask)
		
		contours,hierarchy = cv2.findContours(full_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		largest_contour = max(contours, key=cv2.contourArea)
		x, y, w, h = cv2.boundingRect(largest_contour)
		
		return x, y, w, h, img_shape
		
	def centerObject(self, x, y, w, h, shape):
		alt = (self.drone.get_drone_coordinates())[2]
		
		x_center = shape[1]/2
		y_center = shape[0]/2
		
		x_offset = x + (w/2)
		y_offset = y + (h/2)
		
		x_correction = x_center - x_offset
		y_correction = y_offset - y_center
		
		x_max = 2 * alt * math.tan(LENGTH_ANGLE/2)
		y_max = 2 * alt * math.tan(WIDTH_ANGLE/2)
		
		x_mpp = x_max/shape[1]
		y_mpp = y_max/shape[0]
		
		x_meter_correction = x_correction * x_mpp
		y_meter_correction = y_correction * y_mpp
			
		return x_meter_correction, y_meter_correction

	def yuv_frame_processing(self):
		while self.media.running:
			try:
				yuv_frame = self.media.frame_queue.get(timeout=0.1)
				self.media.frame_counter += 1
				if (self.media.frame_counter % 20) == 0:
					# the VideoFrame.info() dictionary contains some useful information
					# such as the video resolution
					info = yuv_frame.info()

					height, width = (  # noqa
					    info["raw"]["frame"]["info"]["height"],
					    info["raw"]["frame"]["info"]["width"],
					)

					# yuv_frame.vmeta() returns a dictionary that contains additional
					# metadata from the drone (GPS coordinates, battery percentage, ...)

					# convert pdraw YUV flag to OpenCV YUV flag
					cv2_cvt_color_flag = {
						olympe.VDEF_I420: cv2.COLOR_YUV2BGR_I420,
						olympe.VDEF_NV12: cv2.COLOR_YUV2BGR_NV12,
					}[yuv_frame.format()]

					cv2frame = cv2.cvtColor(yuv_frame.as_ndarray(), cv2_cvt_color_flag)
					
					x,y,w,h,shape = self.boundRed(cv2frame)
					x_correction, y_correction = self.centerObject(x,y,w,h,shape)
					self.drone.piloting.move_by(y_correction, x_correction, 0, 0)
				
				#cv2.imwrite(os.path.join(self.download_dir, "test{}.jpg".format(self.frame_counter)), cv2frame)
				
			except queue.Empty:
				continue
		
		# You should process your frames here and release (unref) them when you're done.
		# Don't hold a reference on your frames for too long to avoid memory leaks and/or memory
		# pool exhaustion.
		yuv_frame.unref()	
	
if __name__ == "__main__":
	
	sp = SoftwarePilot()
	drone = sp.setup_drone("parrot_anafi", 1, "None")
	redTracker = RedTracker(drone)
	drone.connect()
	
	drone.camera.media.setup_stream(yuv_frame_processing = redTracker.yuv_frame_processing)
	drone.camera.controls.set_orientation(0, -90, 0, wait=True) # Rotate camera to point downwards
	
	drone.piloting.takeoff()
	
	drone.camera.media.start_stream()
	
	time.sleep(30)
	
	drone.camera.media.stop_stream()
	
	drone.piloting.land()
	
	drone.disconnect()
	

	

	
