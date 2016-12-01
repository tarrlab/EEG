# -*- coding: utf-8 -*-
"""
Written on Thurs Dec 1 2016

@author Austin Marcus - aimarcus@andrew.cmu.edu
Localizer - one-back faces, objects, scenes
500ms stim pres time, 1s ITI
"""

import random
from psychopy import visual, core, event
import numpy
import glob
import cv2
import time

#create a window
mywin = visual.Window([1000, 1000], monitor="testMonitor", units="deg")

#test image
#test_pic = visual.ImageStim(win=mywin, pos=[0,0], image="Stimuli/Faces/AF0303_1110_CO.jpg")

faces = []

face_ims = glob.glob("~/Documents/Projects/EEG_RealTime/Faces/*jpg")
for image in face_ims:
    to_add = cv2.imread(image)
    faces.append(to_add)

random.shuffle(faces)

for face in faces:
    face_display = visual.ImageStim(win=mywin, image=face, pos=[0,0])
    face_display.draw()
    mywin.flip()
    core.wait(0.05)
    
    
