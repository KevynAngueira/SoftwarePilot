import olympe
from olympe.messages.camera import (
	reset_zoom,
	reset_alignment_offsets,
	set_zoom_target,
	set_alignment_offsets,
	alignment_offsets,
)

# << Camera Movementa and Zoom Methods >>
class AnafiCameraControls:
	def __init__(self, drone_object):
		self.drone = drone_object
	
	def reset_zoom(self):
		self.drone(reset_zoom(cam_id = 0)).wait()
	
	def reset_alignment_offsets(self):
		self.drone(reset_alignment_offsets(cam_id = 0)).wait()
	
	# Must be reset before setting zoom again
	def set_zoom(self, target, control_mode = "level"):
		self.drone(set_zoom_target(cam_id = 0, control_mode = control_mode, target = target)).wait()
	
	# Must be reset before setting alignment offsets again
	def set_alignment_offsets(self, yaw, pitch, roll, wait = False):
		if wait == False:
			self.drone(set_alignment_offsets(cam_id = 0, yaw = yaw, pitch = pitch, roll = roll)).wait()
		else:
			self.drone(
				set_alignment_offsets(cam_id = 0, yaw = yaw, pitch = pitch, roll = roll)
				>> alignment_offsets(cam_id = 0, 
					current_yaw = yaw,
					current_pitch = pitch,
					current_roll = roll
				)
			).wait().success()

