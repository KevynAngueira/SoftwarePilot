from fastapi import File, UploadFile, FastAPI
import traceback
import uvicorn
from SoftwarePilot import SoftwarePilot

HOST = "192.168.231.231" # REPLACE: IP for the URL
PORT = 2310 # REPLACE: Port for the URL
INPUT_SHAPE = "None" # REPLACE: the expected input shape
RESPONSE_KEYS = ["key"] # REPLACE: keys to be included in the response, must match response_values
PATH = "None" # REPLACE: Path to download images

app = FastAPI()
drone = None
sp = SoftwarePilot()


@app.get("/")
async def get_port():
	return {"ip": HOST, "port": PORT, "input shape": INPUT_SHAPE, "output keys": RESPONSE_KEYS, "download path": PATH}

@app.get("/ping/")
async def get_ping(p3: str = "-1", p4: int = "-1", p5: str = "-1", p6: str = "-1", p7: str = "-1", p8: str = "-1"):
	try:
		return {"p3": p3, "p4": p4+1000, "p5": p5, "p6": p6, "p7": p7, "p8": p8}
	except:
		return {"result": "failed"}

@app.get("/set/")
async def setDrone(p3: str = "parrot_anafi", p4: int = 1, p5: str = "None"):
	'''
	p3 = drone_type
	p4 = connection_type
	p5 = download_dir
	'''
	global drone
	try:
		drone = sp.setup_drone(p3, p4, p5)
		return {"result" : "Set command sent"}
	except:
		return {"result" : "failed - Unable to set_drone"}

@app.get("/connect/")
async def connect():
	global drone
	if (drone != None):
		try:
			drone.connect()
			return {"result" : "Connect command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}

@app.get("/disconnect/")
async def disconnect():
	global drone
	if (drone != None):
		try:
			drone.disconnect()
			return {"result" : "Disconnect command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}

@app.get("/takeoff/")
async def takeoff():
	global drone
	if (drone != None):
		try:
			drone.piloting.takeoff()
			return {"result" : "Takeoff command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}
	
@app.get("/land/")
async def land():
	global drone
	if (drone != None):
		try:
			drone.piloting.land()
			return {"result" : "Land command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}

@app.get("/move/distance/")
async def move_by(p3:float, p4:float, p5:float, p6:float, p7:bool = False):
	'''
	p3 = x
	p4 = y
	p5 = z
	p6 = angle
	p7 = wait
	'''
	global drone
	if (drone != None):
		try:
			drone.piloting.move_by(p3, p4, p5, p6, p7)
			return {"result" : "MoveBy command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}

@app.get("/move/waypoint/")

async def move_to(p3:float, p4:float, p5:float, p6:str = "None", p7:float = 0, p8:bool = False):
	'''
	p3 = lat
	p4 = lon
	p5 = alt
	p6 = orientation_mode
	p7 = heading
	p8 = wait
	'''
	global drone
	if (drone != None):
		try:
			drone.piloting.move_to(p3, p4, p5, p6, p7, p8)
			return {"result" : "MoveTo command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}

@app.get("/move/distance/cancel/")
async def cancel_move_by():
	global drone
	if (drone != None):
		try:
			drone.piloting.cancel_move_by()
			return {"result" : "MoveByCancel command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}

@app.get("/move/waypoint/cancel/")
async def cancel_move_to():
	global drone
	if (drone != None):
		try:
			drone.piloting.cancel_move_to()
			return {"result" : "MoveToCancel command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}
	
@app.get("/setup/photo/")
async def setup_photo(
	p3:str = "single",
	p4:str = "rectilinear",
	p5:str = "dng",
	p6:str = "burst_14_over_1s",
	p7:str = "preset_1ev",
	p8:float = 0.1
):
	'''
	p3 = mode
	p4 = format
	p5 = file_format
	p6 = burst
	p7 = bracketting
	p8 = capture_interval
	'''
	global drone
	if (drone != None):
		try:
			drone.camera.media.setup_photo(p3, p4, p5, p6, p7, p8)
			return {"result" : "PhotoSetup command sent"}
		except:
			print(traceback.format_exc())        
			return {"result" : "failed"}
	return {"result" : "no drone"}

@app.get("/setup/recording/")
async def setup_recording(
	p3:str = "standard",
	p4:str = "res_dci_4k",
	p5:str = "fps_24",
	p6:str = "ratio_15",
):
	'''
	p3 = mode
	p4 = resolution
	p5 = framerate
	p6 = hyperlapse
	'''
	global drone
	if (drone != None):
		try:
			drone.camera.media.setup_recording(p3, p4, p5, p6)
			return {"result" : "RecordingSetup command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}

@app.get("/setup/streaming/")
async def setup_streaming(
	value:int = 2,
	record:bool = False,
	yuv_frame_processing:str = "None",
	yuv_frame_cb:str = "None",
	h264_frame_cb:str = "None",
	start_cb:str = "None",
	end_cb:str = "None",
	flush_cb:str = "None"
):
	'''
	p3 = value
	p4 = record
	p5 = yuv_frame_processing
	p6 = yuv_fram_cb
	p7 = h264_frame_cb
	p8 = start_cb
	p9 = end_cb
	p10 = flush_cb
	'''
	global drone
	if (drone != None):
		try:
			drone.camera.media.setup_streaming(
				p3, p4, p5, p6, p7, p8, p9, p10
			)
			return {"result" : "StreamingSetup command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}
	
@app.get("/take/photo/")
async def take_photo():
	global drone
	if (drone != None):
		#try:
		drone.camera.media.take_photo()
		return {"result" : "TakePhoto command sent"}
		#except:
		#	return {"result" : "failed"}
	return {"result" : "no drone"}
	
@app.get("/take/recording/start")
async def start_recording():
	global drone
	if (drone != None):
		try:
			drone.camera.media.start_recording()
			return {"result" : "StartRecording command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}
	
@app.get("/take/recording/stop")
async def stop_recording():
	global drone
	if (drone != None):
		try:
			drone.camera.media.stop_recording()
			return {"result" : "StopRecording command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}
	
@app.get("/take/streaming/start")
async def start_streaming():
	global drone
	if (drone != None):
		try:
			drone.camera.media.start_streaming()
			return {"result" : "StartStreaming command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}
	
@app.get("/take/streaming/stop")
async def stop_streaming():
	global drone
	if (drone != None):
		try:
			drone.camera.media.stop_streaming()
			return {"result" : "StopStreaming command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}

@app.get("/download/")
async def download():
	global drone
	if (drone != None):
		try:
			drone.camera.media.download_last_media()
			return {"result" : "Download command sent"}
		except:
			return {"result" : "failed"}
	return {"result" : "no drone"}

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
