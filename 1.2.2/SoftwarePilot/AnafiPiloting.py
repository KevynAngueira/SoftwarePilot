import olympe
from olympe.messages.ardrone3.Piloting import (
	TakeOff,
	Landing,
	moveBy,
	moveTo,
	CancelMoveTo,
	CancelMoveBy,
)
from olympe.messages.ardrone3.PilotingState import (
	FlyingStateChanged,
	PositionChanged,
	moveToChanged,	
)

class AnafiPiloting:
	'''
	Wrapper for the Parrot Olympe flight control methods
	
	...
	
	Attributes
	----------
	drone : olympe.Drone
		the drone object
	action_queue : str[]
		queue of all the actions to be executed
		
	Methods
	-------
	takeoff(queue)
		initiates drone takeoff
	land(queue)
		initiates drone landing
	wait_until_state(state, timeout)
		wait until state is reached
	move_by(x, y, z, angle, wait, queue)
		moves the drone a given number of meters or rotates it to a set angle
	move_to(lat, lon, alt, orientation_mode, heading, wait, queue)
		moves the drone to given waypoint or rotates it to a set angle from north
	cancel_move_by()
		cancels move_by order
	cancel_move_to
		cancels move_to order
	add_action(action)
		adds {action : str} to the {action queue : str[]}
	remove_action(index)
		removes and returns the {action : str} from at position {index : int} from {action_queue : str[]}
	clear_actions()
		clears the {action_queue : str[]}
	execute_actions(num, a_sync)
		Executes the first {num : int} actions from {action_queue : str[]} in order.
	'''
	
	def __init__(self, drone_object):
		'''
		Parameters
		----------
		drone_object : olympe.Drone
			the drone object
		'''
		
		self.drone = drone_object
		self.action_queue = []	

	def takeoff(self, queue = False):
		'''
		Initiates drone takeoff. If {queue : bool} is True send to {action_queue : str[]} instead. 
		
		Parameters
		----------
		queue : bool, optional
			if True send to {action_queue : str[]}, else False execute. (default = False)
		'''
		if queue == False:
			assert self.drone(TakeOff() >> FlyingStateChanged(state = "hovering", _timeout=5)).wait().success()
			print("------ TAKEOFF ------")
		else:
			self.add_action("TakeOff()")
	
	def land(self, queue = False):
		'''
		Initiates drone landing. If {queue : bool} is True send to {action_queue : str[]} instead.
		
		Parameters
		----------
		queue : bool, optional
			if True send to {action_queue : str[]}, else False execute. (default = False)
		'''
		if queue == False:
			assert self.drone(Landing()).wait().success()
			print("------ LAND ------")
		else:
			self.add_action("Landing()")
	
	def wait_until_state(self, state, timeout = None):
		'''
		Sends a wait until given {state : str} instruction to the {action_queue : str[]}
		
		Parameters
		----------
		state : str
			the state to be waited for:
			- "landed"
			- "takingoff"
			- "landing"
			- "hovering"
			- "flying"
		timeout : int
			the time in seconds to wait for state
		'''
	
		if timeout == None:
			self.add_action("FlyingStateChanged('{}')".format(state))
		else:
			self.add_action("FlyingStateChanged('{}', _timeout={})".format(state, timeout))
		# print("------WAITING : {}------".format(state))
	
	def move_by(self, x, y, z, angle, wait = False, queue = False):
		'''
		Moves the drone a given number of meters or rotates it to a set angle.
		If {queue : bool} is True send to {action_queue : str[]} instead.
		
		Parameters
		----------
		x : float
			the movement in the x axis, forwards and backwards, in meters
		y : float
			the movement in the y axis, left and right, in meters
		z : float
			the movement in the z axis, up and down, in meters
		angle : float
			the rotation in radians
		wait : bool, optional
			if true waits for completion before sending the next instruction (default = False)
		queue : bool, optional
			if True send to {action_queue : str[]}, else False execute. (default = False)
		'''
		
		if queue == False:
			if wait == True:
				assert self.drone(moveBy(x, y, z, angle) >> FlyingStateChanged("hovering")).wait().success()
			else:
				self.drone(moveBy(x, y, z, angle))
			print("------ MOVEBY ------")
			print("------ x : {} ------".format(x))
			print("------ Y : {} ------".format(y))
			print("------ Z : {} ------".format(z))
			print("------ ANGLE : {} ------".format(angle))
		else:
			self.add_action("moveBy({}, {}, {}, {})".format(x, y, z, angle))
			if wait == True:
				self.wait_until_state("hovering")		
	
	def move_to(self, lat, lon, alt, orientation_mode = "NONE", heading = 0, wait = False, queue = False):
		'''
		Moves the drone to given waypoint or rotates it to a set angle from north.
		If {queue : bool} is True send to {action_queue : str[]} instead.
		
		Parameters
		----------
		lat : float
			the latitude to travel to
		lon : float
			the longitude to travel to
		alt : float
			the altitude to travel to
		orientation_mode : str, optional
			the orientation mode (default = "NONE")
			- "NONE"
			- "TO_TARGET" (looks at the direction of the given location)
			- "HEADING_START" (Changes orientation before travelling)
			- "HEADING_DURING" (Changes orientation during travel)
		heading : float, optional
			the target orientation dictated by degrees from north (default = 0)
			only used if orientation_mode is "HEADING_START" or "HEADING_DURING"
		wait : bool, optional
			if true waits for completion before sending the next instruction (default = False)
		queue : bool,optional
			if True send to {action_queue : str[]}, else False execute. (default = False)
		'''
		
		if queue == False:
			if wait == True:
				assert self.drone(
					moveTo(latitude=lat,longitude=lon,altitude=alt,orientation_mode=orientation_mode,heading=heading)
					>> FlyingStateChanged("hovering")
				).wait().success()
			else:
				self.drone(
					moveTo(latitude=lat,longitude=lon,altitude=alt,orientation_mode=orientation_mode,heading=heading)
				)
			print("------ MOVETO ------")
			print("------ LAT : {} ------".format(lat))
			print("------ LON : {} ------".format(lon))
			print("------ ALT : {} ------".format(alt))
			print("------ HEADING : {} ------".format(heading))
		else:				
			self.add_action("moveTo(latitude={},longitude={},altitude={},orientation_mode={},heading={})".format(
				lat,lon,alt,orientation_mode,heading
			))
			if wait == True:
				self.wait_until_state("hovering")
		
	def cancel_move_by(self):
		'''
		cancels move_by order
		'''
	
		assert self.drone(CancelMoveBy()).wait()
		
		print("------ CANCEL : MOVEBY ------")

	def cancel_move_to(self):
		'''
		cancels move_to order
		'''
		
		assert self.drone(CancelMoveTo()).wait()
		
		print("------ CANCEL : MOVEBY ------")
	
	def add_action(self, action):
		'''
		adds {action : str} to the {action queue : str[]}
		
		Parameters
		----------
		action : str
			The action to be added
		'''
		self.action_queue.append(action)

	def remove_action(self, index):
		'''
		removes and returns the {action : str} from at position {index : int} from {action_queue : str[]}
	
		Parameters
		----------
		index : int
			The index to remove the action at
		
		Return
		----------
		action : str
			the removed action
		'''
		return self.action_queue.pop(index)

	def clear_actions(self):
		'''
		clears the {action_queue : str[]}
		'''
		self.action_queue = []
		
	def execute_actions(self, num = -1, a_sync = False):
		'''
		Executes the first {num : int} actions from {action_queue : str[]} in order.
		If {a_sync : bool} is False wait until completion, else True run flight path asyncronously.
		
		Parameters
		----------
		num : int, optional
			The number of instructions to execute (default = all)
		a_sync : bool, optional
			If {a_sync : bool} is False wait until completion, else True run flight path asyncronously.
		'''
		if num < 0:
			num = len(self.action_queue)
		
		flight_path = "self.drone("
		for i in range(num):
			action = self.action_queue.pop(0)
			flight_path += action
			if i < num-1:
				flight_path += ">>"
		flight_path += ")"
		if a_sync == False:
			flight_path += ".wait()"
		
		print("------ EXECUTE ACTIONS : Start ------")
		print(flight_path)
		print("------ EXECUTE ACTIONS : End ------")
		eval(flight_path)
		
