from fastapi import File, UploadFile, FastAPI
import uvicorn
# ADD: libraries to import
import cv2
import os
import math

HOST = "0.0.0.0" # REPLACE: IP for the URL
PORT = 8000 # REPLACE: Port for the URL
INPUT_SHAPE = [4608, 3456] # REPLACE: the expected input shape
RESPONSE_KEYS = ['x', 'y', 'z', 'angle'] # REPLACE: keys to be included in the response, must match response_values
PATH = "None" # REPLACE: Path to download images

# ADD: Setup code
cascPath = "app/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)


app = FastAPI()

@app.get("/")
async def get_port():
	return {"ip": HOST, "port": PORT, "input shape": INPUT_SHAPE, "output keys": RESPONSE_KEYS, "download path": PATH}

@app.post("/image/")
async def upload(file: UploadFile = File(...)):
	
	if PATH != "None":
		filepath = os.path.join(PATH, file.filename)
	else:
		filepath = file.filename
			
	try:
		contents = await file.read()			
		with open(filepath, 'wb') as f:
			f.write(contents)

	except Exception:
		return {"message": "There was an error uploading the file"}
	finally:
		await file.close()				
		
		# ADD: Custom code, should return a values list that matches the response_keys
		image = cv2.imread(filepath)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		faces = faceCascade.detectMultiScale(
		    		gray,
		    		scaleFactor=1.1,
				minNeighbors=5,
				minSize=(30, 30),
				#flags = cv2.cv.CV_HAAR_SCALE_IMAGE
		)
		if len(faces) != 0:
			target_bb = faces[0]
			
			target_area = (target_bb[2])*(target_bb[3])
			target_fraction = target_area/(INPUT_SHAPE[0] * INPUT_SHAPE[1])
			x_offset = 0.05 - target_fraction
			y_offset = (target_bb[0]+(target_bb[2]/2))-(INPUT_SHAPE[0]/2)
			z_offset = (target_bb[1]+(target_bb[3]/2))-(INPUT_SHAPE[1]/2)
			
			response_values = [x_offset*2.5, y_offset/1000, z_offset/2000, 0]
		else:
			response_values = [0, 0, 0, math.pi/8]
		# REPLACE: values to be included in the response from custom code, must match responce_keys
		
		response = dict(zip(RESPONSE_KEYS, response_values))
	
	return response

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
