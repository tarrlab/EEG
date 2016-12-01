# -*- coding: utf-8 -*-
"""
Written on Thurs Dec 1 2016

@author Austin Marcus - aimarcus@andrew.cmu.edu
Localizer - one-back faces, objects, scenes
500ms stim pres time, 1s ITI
"""

import random
from psychopy import visual, core, event
import glob
import cv2
import time

#create a window
mywin = visual.Window([800, 800], monitor="testMonitor", units="deg")

#load faces
faces = []

face_ims = glob.glob("/home/austin/Documents/Projects/EEG_RealTime/Stimuli/Faces/*.jpg")

for image in face_ims:
    faces.append(image)

#load objects
objects = []

object_ims = glob.glob("/home/austin/Documents/Projects/EEG_RealTime/Stimuli/Objects/*.jpg")

for image in object_ims:
    objects.append(image)
    
#load scenes
scenes = []

scene_ims = glob.glob("/home/austin/Documents/Projects/EEG_RealTime/Stimuli/Scenes/*.jpg")

for image in scene_ims:
    scenes.append(image)

#shuffle everything
random.shuffle(faces)
random.shuffle(objects)
random.shuffle(scenes)

last_shown = ""

faces_shown = 0
objects_shown = 0
scenes_shown = 0
total_shown = 0

#core program
while total_shown < 280:
    
    
mywin.close()
core.quit()

    
