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
from collections import defaultdict
from itertools import islice
import linecache

# mavic pro camera properties
FOV = 78.8 #Mavic Pro camer field of view 78.8 Deg
CROP_FACTOR = 35/26
IMAGE_WIDTH = 4000 #pixels
IMAGE_HEIGHT = 3000 #pixels
STEP_OVER_ALTITUDE  = 200. #feet
EPS = 1.0E-1
N_ROWS = 197
root = tkinter.Tk()


def get_directory_name(caption):
    dirname = filedialog.askdirectory(parent=root,initialdir="/",title=caption)
    if len(dirname ) > 0:
        print (' You chose %s' % dirname)
    return dirname
def get_file_name(caption):
    file = filedialog.askopenfile(parent=root,mode='rb',title=caption)
    if file != None:
        data = file.read()
    #file.close()
    print (' I got %d bytes from this file.' % len(data))
    return file

def save_file_name(caption):
    myFormats = [
    ('Windows Bitmap','*.bmp'),
    ('Portable Network Graphics','*.png'),
    ('JPEG / JFIF','*.jpg'),
    ('CompuServer GIF','*.gif'),
    ]
    fileName = filedialog.asksaveasfilename(parent=root,filetypes=myFormats ,title=caption)
    if len(fileName ) > 0:
        print ('Now saving under %s"' % nomFichier)
    return fileName   

def make_sorties(wpf_name):
    MAX_SORTIE_LENGTH = 90
    n_lines = 197    # ONLY FOR THIS TEST CASE
    #this_line = defaultdict(list)
    fieldnames_1 = []
    length_base_file_name = len(wpf_name)
    base_file_name = wpf_name[:length_base_file_name-4]
    sortie = 1
    start_line = 1
    stop_line = 90
    line_count = 0
    row_number = 0
    keys_1 = []
    n_sorties = math.ceil(n_lines/MAX_SORTIE_LENGTH)
    sortie_length = math.ceil(n_lines/n_sorties)

    with open(wpf_name,'r') as csvfile:
        reader = csv.DictReader(csvfile,dialect='excel')
        fieldnames_1 = reader.fieldnames
        #print ('fieldnames_1[0]',fieldnames_1[0])
        #print ('fieldnames',fieldnames_1)
        for row in reader:
            #this_line = row
            #print('row_number: ',row_number,' this_line[altitude]',this_line[fieldnames_1[2]], '\n')
            #print('this_line ',(this_line.values()))
            if row_number%sortie_length == 0:
                sortie_file_name = base_file_name + '_sortie_' + str(sortie) + '.csv'
                f_csv = open(sortie_file_name,'w',newline ='\n')
                print('row_number ',row_number)
                writer = csv.DictWriter(f_csv,fieldnames_1,dialect='excel')
                writer.writeheader()
                if abs(float(row[fieldnames_1[2]]) - STEP_OVER_ALTITUDE) > EPS:
                    altitude = row[fieldnames_1[2]]
                    stepover_row = row
                    stepover_row[fieldnames_1[2]] = STEP_OVER_ALTITUDE
                    stepover_row[fieldnames_1[12]] = -1
                    writer.writerow(stepover_row)
                    row[fieldnames_1[2]] = altitude
                    row[fieldnames_1[12]] = 1

            writer.writerow(row)
            #writer.writerow(this_line.values())
            if (row_number%sortie_length == sortie_length -1):
                sortie += 1
                if abs(float(row[fieldnames_1[2]]) - STEP_OVER_ALTITUDE) > EPS:
                    stepover_row = row
                    stepover_row[fieldnames_1[2]] = STEP_OVER_ALTITUDE
                    stepover_row[fieldnames_1[12]] = -1
                    writer.writerow(stepover_row)
                f_csv.close()

            row_number += 1
        print ('keys_1 ',keys_1)
        #print ('fieldnames_1 ',fieldnames_1)
        print ('fieldnames_1[2] ',fieldnames_1[2])

    return
    
def problem_1():
    # get wapoint file name file
    print (' Please browse waypoint file')
    waypoint_file = get_file_name(' Please browse for border point file ')
    wpf_name = waypoint_file.name
    make_sorties(wpf_name)
    return

def main():
    problem_1()
    print ('Done at last')
    xit = input('Enter any key to exit: ')
    return

main()

if __name__ == "main":
     # execute only if run as a script
     main()
