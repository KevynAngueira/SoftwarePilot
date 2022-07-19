from fastapi import File, UploadFile, FastAPI
import uvicorn
# ADD: libraries to import

HOST = "192.168.0.21" # REPLACE: IP for the URL
PORT = 8000 # REPLACE: Port for the URL
INPUT_SHAPE = "None" # REPLACE: the expected input shape
RESPONSE_KEYS = ["key"] # REPLACE: keys to be included in the response, must match response_values
PATH = "None" # REPLACE: Path to download images

# ADD: Setup code

app = FastAPI()

@app.get("/")
async def get_port():
	return {"ip": HOST, "port": PORT, "input shape": INPUT_SHAPE, "output keys": RESPONSE_KEYS, "download path": PATH}

@app.post("/image/")
async def upload(file: UploadFile = File(...)):
	try:
		contents = await file.read()
		if PATH != "None":
			with open((PATH + file.filename), 'wb') as f:
				f.write(contents)
		else:
			with open(file.filename, 'wb') as f:
				f.write(contents)

	except Exception:
		return {"message": "There was an error uploading the file"}
	finally:
		await file.close()				
		
		# ADD: Custom code, should return a values list that matches the response_keys
		response_values = ["value"] # REPLACE: values to be included in the response from custom code, must match responce_keys
		
		response = dict(zip(RESPONSE_KEYS, response_values))
	
	return response

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
