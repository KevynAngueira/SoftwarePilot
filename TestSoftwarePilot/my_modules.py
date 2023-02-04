"""
My commenly used Modules:
(1) get_directory_name(caption)   -- browses for directory name
(2) get_file_name(caption)  -- browses for a specific file
(3) save_file_name(caption)  -- saves named file to selected directory
(4) get_exif(fn) -- gets inag exif data
(5) get_gps_deg(exf) -- extracts GPS data from exif
(6) get_r_of_phi(gps)  -- given gps coordinase calaculate Polar and Lateral radius of earth in feet
(7) calculate_distance(end_gps_deg,start_gps_deg) -- Calculates distance in feet between 2 GPS coordinats
(8) date_to_nth_day(date, format='%Y\%m\%d')  -- calculates days since begining of year
(9) calculate_sun_angle(gps_deg,dt) -- calculates sun angle (declination and azmeth)
(10)
"""

import tkinter
from tkinter import *
from tkinter import filedialog


import PIL
from PIL import Image,ImageChops
from PIL.ExifTags import TAGS

from DateTime import DateTime
from datetime import datetime
import pandas as pd
import numpy
import math

root = tkinter.Tk()
FOV = 78.8 #Mavic Pro camer field of view 78.9 Deg
EarthMeanRadius  =   6371.01	# In km
AstronomicalUnit  =  149597890	# In km

def get_directory_name(caption):
    dirname = tkinter.filedialog.askdirectory(parent=root,initialdir="/",title=caption)
    if len(dirname ) > 0:
        print (' You chose %s' % dirname)
    return dirname

def get_file_name(caption):
    file = tkinter.filedialog.askopenfile(parent=root,mode='rb',title=caption)
    if file != None:
        data = file.read()
    #file.close()
    print (" I got %d bytes from this file." % len(data))
    return file

def save_file_name(caption):
    myFormats = [
    ('Windows Bitmap','*.bmp'),
    ('Portable Network Graphics','*.png'),
    ('JPEG / JFIF','*.jpg'),
    ('CompuServer GIF','*.gif'),
    ]
    fileName = tkinter.filedialog.asksaveasfilename(parent=root,filetypes=myFormats ,title=caption)
    if len(fileName ) > 0:
        print ('Now saving under %s' % nomFichier)
    return fileName

def get_exif(fn):
    ret = {}
    i = PIL.Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        #print('decoded',decoded)
        ret[decoded] = value
    return ret

def get_gps_deg(exf):
    GPS = []
    gps = exf['GPSInfo']
    GPS0 = float(gps[2][0][0])/float(gps[2][0][1]) + float(gps[2][1][0])/(60.*float(gps[2][1][1])) + float(gps[2][2][0])/(3600*float(gps[2][2][1]))
    if (gps[1] == u'S'):
        GPS0 = -GPS0
    GPS.append(GPS0)
    GPS1 = float(gps[4][0][0])/float(gps[4][0][1]) + float(gps[4][1][0])/(60.*float(gps[4][1][1])) + float(gps[4][2][0])/(3600*float(gps[4][2][1]))
    if (gps[3] == u'W'):
        GPS1 = -GPS1
    GPS.append(GPS1)
    GPS2 = float(gps[6][0])/float(gps[6][1])
    GPS.append(GPS2)
    return GPS

def get_r_of_phi(gps):
    phi = (math.pi/180.)*gps[0]
    a = 7923.00*2640  # Equatorial radius of earth in feet
    b = 7899.86*2640  # Polar radius of earth in feet
    r = []
    r1 = a*b/math.sqrt(a*a - (a*a - b*b)*math.cos(phi))
    r.append(r1)
    r2 = r1*math.cos(phi)
    r.append(r2)
    #print 'r = ',r
    return r

def calculate_distance(end_gps_deg,start_gps_deg):
    r = get_r_of_phi(start_gps_deg)
    delta_0 = (math.pi/180)*r[0]*(end_gps_deg[0] - start_gps_deg[0])
    delta_1 = (math.pi/180)*r[1]*(end_gps_deg[1] - start_gps_deg[1])
    #dist = math.sqrt(delta0*delta0 + delta1*delta1)
    return [delta_0,delta_1]

def date_to_nth_day(date, format='%Y\%m\%d'):
        date = pd.to_datetime(date, format=format)
        new_year_day = pd.Timestamp(year=date.year, month=1, day=1)
        return (date - new_year_day).days + 1

def calculate_sun_angle(gps_deg,dt):    
    t = DateTime(dt) # Day of year calculation
    n = date_to_nth_day(t.Date())
    #print 'Day of the year', n
    azimuth_angle  = 0.
    solar_noon = 8.0 - (24.0/360.0)*gps_deg[1] #  8 = GMT-4 + 12 for 24 hour clock
    angle_hour = DateTime.hour(dt) + DateTime.minute(dt)/60 + DateTime.second(dt)/3600 - solar_noon
    hour_angle = (math.pi/180.)*15.0*angle_hour
    #print 'solar noon', solar_noon, ' now ', dt, ' angle_hour ',angle_hour,' hour_angle ',hour_angle 
    declination_angle = 23.45*(math.pi/180.)*math.sin((math.pi/180.)*360.0*(284.0+n)/365.0)
    #print 'day ', n,'declination_angle', (180.0/math.pi)*declination_angle
    sin_declination_angle = math.sin(declination_angle) 
    cos_declination_angle = math.cos(declination_angle)
    latitude_angle = (math.pi/180.)*gps_deg[0]
    cos_latatude_angle = math.cos(latitude_angle)
    sin_latatude_angle = math.sin(latitude_angle)
    cos_hour_angle     = math.cos(hour_angle)
    altitude_angle     = cos_latatude_angle*cos_hour_angle*cos_declination_angle
    altitude_angle    += sin_declination_angle*sin_latatude_angle
    altitude_angle     = math.asin(altitude_angle)
    #altitude_angle     = (math.pi/180.0)*52.17
    dY                 = -math.sin(hour_angle)
    dX                 = math.tan(declination_angle)*cos_latatude_angle - sin_latatude_angle*cos_hour_angle
    azimuth_angle      = math.atan2(dY,dX)   
    if (azimuth_angle < 0.0):
       azimuth_angle  +=  2.0*math.pi
    # parallax correction
    Parallax=(EarthMeanRadius/AstronomicalUnit)*math.sin(altitude_angle)
    #print 'Parallax',Parallax
    #azimuth_angle += Parallax
    # in km but that dosent matter since it only used as a rartio
    #print 'altitude_angle',(180./math.pi)*altitude_angle, ' azimuth_angle ',(180./math.pi)* azimuth_angle 
    return [altitude_angle, azimuth_angle]

