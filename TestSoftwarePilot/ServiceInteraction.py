from SoftwarePilot import SoftwarePilot
import time

'''
This is a short demo demonstrating how to boot up a dockerized service and requesting it with SoftwarePilot

SoftwarePilot provides a python template of a Rest API which the user is meant to modify and dockerize
This API is meant to offload the image processing workload to a more capable machine
SoftwarePilot does not limit the service to which it will connect to, but the basic structure must be followed for proper behavior
'''

sp = SoftwarePilot()

sp.setup_docker()
time.sleep(5)
# REPLACE : DOCKER_IMAGE
container = sp.docker.deploy_container("DOCKER_IMAGE", detach = True, ports = {8000:8000})

ip_host = sp.get_host_ip()
service = sp.setup_service(ip_address = ip_host)

response = service.get()
print(response)

# REPLACE : IMAGE_PATH
response = service.run("IMAGE_PATH")
print(response)
