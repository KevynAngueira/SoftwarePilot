import olympe
from olympe.messages.camera import (
	reset_zoom,
	reset_alignment_offsets,
	set_zoom_target,
	set_alignment_offsets,
	alignment_offsets,
)
from olympe.messages.auto_look_at import start, stop
from olympe.messages.gimbal import set_target, attitude

# << Camera Movementa and Zoom Methods >>
class AnafiCameraControls:
	'''
	Wrapper for the Parrot Olympe camera methods involving camera controls
	
	...
	
	Attributes
	----------
	drone : olympe.Drone
		the drone object
		
	Methods
	-------
	reset_zoom()
		resets the drone's camera zoom
	reset_orientation()
		resets the drone's camera's orientation
	set_zoom(target, control_mode)
		sets the drone's camera zoom, must call reset_zoom before being called again
	set_orientation(yaw, pitch, roll, reference, wait)
		sets the drone's camera alignment offset
	wait_until_orientation(yaw, pitch, roll, timeout)
	'''

	def __init__(self, drone_object):
		'''
		Parameters
		----------
		drone_object : olympe.Drone
			the drone object
		'''
		
		self.drone = drone_object
		self.drone(start(1))
	
	def reset_zoom(self):
		'''
		resets the drone's camera's zoom
		'''
		
		self.drone(reset_zoom(cam_id = 0)).wait()
	
	def reset_orientation(self):
		'''
		resets the drone's camera's orientation
		'''
		
		self.drone(set_target(
			gimbal_id = 0,
			control_mode = 0,
			yaw_frame_of_reference = 1,
			yaw = 0,
			pitch_frame_of_reference = 1,
			pitch = 0,
			roll_frame_of_reference = 1,
			roll = 0,
		))

	def set_zoom(self, target, control_mode = "level"):
		'''
		sets the drone's camera's zoom, must call reset_zoom before being called again
		
		Parameters
		----------
		target : float
			the level or velocity of zoom
		control_mode : str, optional
			the target interpretation (default = "level")
			- "level"/"velocity"
		'''
		
		self.drone(set_zoom_target(cam_id = 0, control_mode = control_mode, target = target)).wait()
	
	def set_orientation(self, yaw, pitch, roll, reference = 1, wait = False):
		'''
		Sets the drone's camera's orientation
		
		Parameters
		----------
		yaw : float
			the yaw camera offset (degrees)
		pitch : float
			the pitch camera offset (degrees)
		roll : float
			the roll camera offset (degrees)
		reference : int or str, optional
			the reference mode used for camera orientation (default 1)
			- 0 or "NONE" (from current orientation)
			- 1 or "RELATIVE" (roll : forward - pitch : right - yaw : down) 
			- 2 or "ABSOLUTE" (roll : North - pitch : East - yaw : Center of Earth)
		wait : bool, optional
			if True wait until completion before next instruction (default False)
		'''
		self.drone(set_target(
			gimbal_id = 0,
			control_mode = 0,
			yaw_frame_of_reference = reference,
			yaw = yaw,
			pitch_frame_of_reference = reference,
			pitch = pitch,
			roll_frame_of_reference = reference,
			roll = roll,
		))
		
		if wait == True:
			assert self.drone(attitude(
				gimbal_id = 0,
				yaw_relative = yaw,
				pitch_relative = pitch,
				roll_relative = roll,
			)).wait().success()
	
	def wait_until_orientation(self, yaw, pitch, roll, timeout=5):
		'''
		Waits until given gimbal orientation. Returns True if orientation is reached before {timeout : int}, False otherwise.

		
		Parameters
		----------
		yaw : float
			the yaw camera offset (degrees)
		pitch : float
			the pitch camera offset (degrees)
		roll : float
			the roll camera offset (degrees)
		timeout : int, optional
			the timeout time before returning False
			
		Return
		----------
		orientation_reached : bool
			Return True if orientation is reached before {timeout : int}, False otherwise.
		'''
	
		orientation_reached = self.drone(attitude(
				gimbal_id = 0,
				yaw_relative = yaw,
				pitch_relative = pitch,
				roll_relative = roll,
			)).wait(_timeout = timeout).success()
		return orientation_reached
