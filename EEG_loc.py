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
#import time

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

#program control
num_blocks = 5

#block loop
cur_block = 1
while cur_blocks <= 5:
    
    #initialize helper variables for each block
    #max 90 faces, 45 objects, 45 scenes
    #total 200 stimuli shown per block, 20 repeated
    last_shown = ""
    faces_shown = 1
    objects_shown = 1
    scenes_shown = 1
    total_shown = 0
    
    #shuffle everything
    random.shuffle(faces)
    random.shuffle(objects)
    random.shuffle(scenes)
    
    #get new random one-back matrix
    oneback_matrix = [0] * 180
    
    for i in range(0,180,10):
        oneback_matrix[i] = 1
    
    #first image shown can't be a repeat, so
    #shuffle until first index is 0
    while oneback_matrix[1] == 1:
        random.shuffle(oneback_matrix)
    
    #core program loop
    while total_shown < 180:
        #if we've reached a one-back condition, display the last 
        #image that was displayed
        if oneback_matrix[total_shown] == 1:
            to_display = last_shown
        else:
            rand = random.randint(1,3)
            if rand == 1:
                #first, check that face count hasn't maxed out
                if faces_shown > 90:
                    continue
                #show a face
                to_display = faces[faces_shown]
                faces_shown += 1
            else if rand == 2:
                #first, check that object count hasn't maxed out
                if objects_shown > 45:
                    continue
                #show an object
                to_display = objects[objects_shown]
                objects_shown += 1
            else:
                #first, check that scene count hasn't maxed out
                if scenes_shown > 45:
                    continue
                #show a scene
                to_display = scenes[scenes_shown]
                scenes_shown += 1
                
        #whichever image was chosen, display it
        display = visual.ImageStim(win=mywin, image=to_display, ) 
        
        #if not a one-back condition, save the most recently-displayed
        #image, and increment the total per-block stim counter
        if oneback_matrix[total_shown] == 0:
            last_shown = to_display
            total_shown += 1
            
mywin.close()
core.quit()

    
