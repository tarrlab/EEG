# -*- coding: utf-8 -*-
"""
Written on Thurs Dec 1 2016

@author Austin Marcus - aimarcus@andrew.cmu.edu
Localizer - one-back faces, objects, scenes
500ms stim pres time, 1s ITI
"""

import random, datetime, time, glob, cv2
from psychopy import visual, core, event, data


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

#instruction text
intro_text = visual.TextStim(win=mywin, 
                             text="Press the space bar if an image repeats.",
                             wrapWidth=20,
                             alignHoriz='center',
                             alignVert='center')

intro_text.draw()
mywin.flip()

#wait for keypress
presses = event.waitKeys()

#begin experiment
begin_text = visual.TextStim(win=mywin, 
                             text="Press any key to begin.",
                             wrapWidth=20,
                             alignHoriz='center',
                             alignVert='center')

begin_text.draw()
mywin.flip()

#wait for keypress
presses = event.waitKeys()
    

#define the fixation display
fixation = visual.ShapeStim(win=mywin, vertices=((0,-8), (0,8), (0, 0), (8, 0), (-8, 0)),
                            lineWidth=2,
                            size=.05,
                            closeShape=False)

#define the break-signalling fixation
break_fix = visual.ShapeStim(win=mywin, vertices=((0,-8), (0,8), (0, 0), (8, 0), (-8, 0)),
                            lineWidth=2,
                            size=.05,
                            closeShape=False,
                            lineColor='black')
#program control
num_blocks = 5

#block loop
cur_block = 1
while cur_block <= 5:
    
    #initialize helper variables for each block
    #max 90 faces, 45 objects, 45 scenes
    #total 200 stimuli shown per block, 20 repeated
    last_shown = ""     #save recent image for one-back condition
    faces_shown = 0     #track total faces shown
    objects_shown = 0   #track total objects shown
    scenes_shown = 0    #track total scenes shown
    total_shown = 0     #track total stims seen by participant
    stims_shown = 0     #track total distinct stims shown
    
    #shuffle everything
    random.shuffle(faces)
    random.shuffle(objects)
    random.shuffle(scenes)
    
    #get new random one-back matrix
    oneback_matrix = [0] * 200
    
    for i in range(0,200,10):
        oneback_matrix[i] = 1
    
    #first image shown can't be a repeat, so
    #shuffle until first index is 0
    while oneback_matrix[0] == 1:
        random.shuffle(oneback_matrix)
    
    fixation.draw()
    mywin.flip()
    core.wait(5.0)
    
    #core program loop
    while stims_shown < 180 and total_shown < 200:
        #if we've reached a one-back condition, display the last 
        #image that was displayed
        if oneback_matrix[total_shown] == 1:
            to_display = last_shown
        else:
            rand = random.randint(1,3)
            if rand == 1:
                #first, check that face count hasn't maxed out
                if faces_shown >= 90:
                    continue
                #show a face
                to_display = faces[faces_shown]
                faces_shown += 1
            elif rand == 2:
                #first, check that object count hasn't maxed out
                if objects_shown >= 45:
                    continue
                #show an object
                to_display = objects[objects_shown]
                objects_shown += 1
            else:
                #first, check that scene count hasn't maxed out
                if scenes_shown >= 45:
                    continue
                #show a scene
                to_display = scenes[scenes_shown]
                scenes_shown += 1
                
        #whichever image was chosen, display it
        display = visual.ImageStim(win=mywin, image=to_display, units="pix", size=250) 
        display.draw()
        mywin.flip()
        core.wait(0.5)
        fixation.draw()
        mywin.flip()
        
        #get reaction time
        timeBefore = time.time()
        presses = event.waitKeys(1.0)
        timeAfter = time.time()
        trial_rt = timeAfter - timeBefore
        
        if(presses and presses[0] == "space" and oneback_matrix[total_shown] == 1):
            #correct response, handle 
            print "Correct!"
        else:
            #incorrect response, handle
            print "Incorrect response"
        
        #if not a one-back condition, save the most recently-displayed
        #image, and increment the total per-block stim counter
        if oneback_matrix[total_shown] == 0:
            last_shown = to_display
            stims_shown += 1
        total_shown += 1
            
        #wait out the remaining time
        core.wait(1.0 - trial_rt)
        
        #break every 25 trials
        if total_shown % 25 == 0:
            break_fix.draw()
            mywin.flip()
            presses = event.waitKeys()
            fixation.draw()
            mywin.flip()
            core.wait(2.0)
    
    wait_text = visual.TextStim(win=mywin, text="You have finished this block. Press any key to continue.")
    
    presses = event.waitKeys()
    if presses:
        cur_block += 1
        continue
            
mywin.close()
core.quit()

    
