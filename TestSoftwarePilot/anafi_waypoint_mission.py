''' 
Given a CSV file containing waypoint data,this Code implements a Wapoint mission on an anafi parrot sUAV. The code is adapted from a sample
program written by Kevyn Angueira.

John Chumley 28OCT2022

'''

from SoftwarePilot import SoftwarePilot
# from MyModules import *
'''
import PIL
from PIL import Image,ImageChops
from PIL.ExifTags import TAGS
import matplotlib.pyplot as plt
import pylab
import tkinter
from tkinter import *
from tkinter import filedialog
import seaborn as sns
import os
import cv2
from DateTime import DateTime
from datetime import datetime
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.path import Path
import csv
import scipy
from scipy.ndimage.filters import gaussian_filter

import collections
from itertools import islice
import linecache
import time

'''

'''
# TODO Replace with actual adafi camers parameters
# Adafi parrot camera properties
FOV = 78.8 # Camera field of view 78.8 Deg
CROP_FACTOR = 35/26 # Lense apature
IMAGE_WIDTH = 4000 # pixels
IMAGE_HEIGHT = 3000 # pixels
STEP_OVER_ALTITUDE  = 200.0 # feet
'''

'''
root = tkinter.Tk()
import my_modules as my_modules
from my_modules import get_directory_name as get_directory_name
from my_modules import get_file_name as get_file_name
from my_modules import save_file_name as save_file_name
#from my_modules import get_exif as get_exif
from my_modules import get_gps_deg as get_gps_deg
from my_modules import get_r_of_phi as get_r_of_phi
from my_modules import calculate_distance as calculate_distance
#from my_modules import date_to_nth_day as date_to_nth_day
#from my_modules import calculate_sun_angle as calculate_sun_angle
#from my_modules import date_to_nth_day as date_to_nth_day
'''

sp = SoftwarePilot()

#sp.setup_docker()

# REPLACE : Docker image name
#container = sp.docker.deploy_container("CUSTOM_DOCKER_IMAGE", detach = True, ports = {8000:8000})

#time.sleep(5)

#ip_host = sp.get_host_ip()
#service = sp.setup_service(ip_address = ip_host)
#service.get()

#download_dir = service.get_download_path()
#drone = sp.setup_drone("parrot_anafi", 1, "None")


drone = sp.setup_drone("parrot_anafi", 1, "None")
drone.connect()
# get wapoint settings file
'''
print ('browse for waypoint settings file')
    wpsf_name = get_file_name('browse for waypoint settings file')
    wpsf_name = WAYPOINT_SETTINGS.name
'''
'''
# TODO parse waypoint settings file for:
	# LOST_SIGNAL_ACTION (NONE|FINISH_MISSION|RETURN_HOME|LAND)
	# AIR_SPEED (mph)
	# END_MISSION_ACTION (NONE|RETURN_HOME|LAND)
	# CLEARANCE_ALTITUDE (ft)
	# SAFE_DISTANCE (ft)
	# HEADING_MODE (NEXT_WAYPOINT|NORTH|SOUTH|EAST|WEST|<DEG>)
	# TURN_DIRECTION (CW|CCW)
	# etc.
with open(wpsf_name,'r') as csvfile:
        reader = csv.DictReader(csvfile,dialect='excel')
        fieldnames_1 = reader.fieldnames
        #print ('fieldnames_1[0]',fieldnames_1[0])
        #print ('fieldnames',fieldnames_1)
        for row in reader:
            #this_line = row
            #print('row_number: ',row_number,'this_line[LOST_SIGNAL_ACTION]',this_line[fieldnames_1[2]], '\n')
            #print('this_line ',(this_line.values()))

'''
# get waypoint file directory
'''
print ('browse for directory to store waypoint file')
    Waypoint_Dir = get_directory_name('Please Select Waypoint Directory')
    Waypoint_filename = input(' Enter Way Point file name: ')
    Waypoint_file = Waypoint_Dir + '/' + Waypoint_filename + '.csv'
'''
# get doirectory to hold images
'''
image_directory = get_directory_name('browse for directory to hold images')
'''
# loop on waypoints
for each waypoint in Waypoint_file

##### read wapoint #####
##### fly to GPS coordinate #####
##### execute wp actions ######
# end loop on waypoints
# return home
# land drone 

drone.camera.media.setup_photo()
drone.piloting.takeoff()
time.sleep(15)

num_img = 0
#while (num_img < 5):
#	drone.camera.media.take_photo()
#	image_path = drone.camera.media.download_last_media()
	
	#response = service.run(image_path)
	#print(response)
	#drone.piloting.move_by(response['x'], response['y'], response['z'], response['angle'])
	
#	num_img += 1

drone.piloting.land()	

drone.disconnect()
