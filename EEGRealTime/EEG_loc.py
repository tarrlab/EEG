# -*- coding: utf-8 -*-
"""
Written on Thurs Dec 1 2016
@author Austin Marcus - aimarcus@andrew.cmu.edu
Localizer - one-back faces, objects, scenes
500ms stim pres time, 1s ITI
"""

import random, datetime, time, glob, cv2
from psychopy import visual, core, event, data, gui
from ctypes import windll

#set up parport for triggering
pport = windll.inpoutx64
pport_addr = 0xcff8

#get subject info from dialog box
dialog = gui.Dlg(title="EEG Realtime Localizer")
dialog.addText("Subject Info")
dialog.addField("Subject ID:")
dialog.addField("Age:")
dialog.addField("Handedness:")

subj_info = dialog.show()

#while not subj_info.OK:
#    subj_info = dialog.show()

subj_id = subj_info[0]
subj_age = subj_info[1]
subj_hand = subj_info[2]    
    
#start data file
datafile = open("Subject{}_EEGRealtimeLocalizer_log.txt".format(subj_id), "w+")
datafile.write("\t\t\t\t\t\t\tEEG Realtime Localizer: Experiment log")
datafile.write("\n")
datafile.write("Current time and date: {}\n".format(datetime.datetime.now()))
datafile.write("Subject info:\n")
datafile.write("ID: {}\tAge: {}\tHandedness: {}".format(subj_id, subj_age, subj_hand))
datafile.write("\n")
datafile.write("Block\t" \
               "Trial#\t" \
               "StimType\t" \
               "OneBack?\t" \
               "Correct?\t" \
               "RT\t" \
               "StimStart\t" \
               "StimDur\t\t" \
               "FixStart\t" \
               "FixDur\n")
                            
#create a window
mywin = visual.Window([800, 800], monitor="testMonitor", units="deg")

########################
####load in stimuli#####
########################

#update all paths as necessary

#load faces
faces = []
face_ims = glob.glob("C:/ExperimentData/YingYang/Real_time/Initial_test_script/Stimuli/Faces/*.jpg")

for image in face_ims:
    faces.append(image)

#load objects
objects = []
object_ims = glob.glob("C:/ExperimentData/YingYang/Real_time/Initial_test_script/Stimuli/Objects/*.jpg")

for image in object_ims:
    objects.append(image)
    
#load scenes
scenes = []
scene_ims = glob.glob("C:/ExperimentData/YingYang/Real_time/Initial_test_script/Stimuli/Scenes/*.jpg")

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
    #shuffle until first index is 0, and 
    #until no two one-back conditions are within 
    #5 trials of each other
    checked = False
    while checked == False:
        if oneback_matrix[0] == 1:
            random.shuffle(oneback_matrix)
            continue
        tooclose = False
        for i in range(0,196):
            #check if one-back conditions within 5 trials
            if oneback_matrix[i] == 1 and \
               (oneback_matrix[i+4] == 1 or \
               oneback_matrix[i+3] == 1 or \
               oneback_matrix[i+2] == 1 or \
               oneback_matrix[i+1] == 1):
                   #reshuffle and start over
                   random.shuffle(oneback_matrix)
                   tooclose = True
                   break
        if tooclose == True:
            continue
        else:
            checked = True
    
    fixation.draw()
    mywin.flip()
    
    #get start time
    exp_start_time = time.time()
    
    core.wait(5.0)
    
    #core program loop
    while stims_shown < 180 and total_shown < 200:
        #if we've reached a one-back condition, display the last 
        #image that was displayed
        if oneback_matrix[total_shown] == 1:
            to_display = last_shown
            #set trigger value
            trig_val = 256
            stim_type = "Repeat"
            oneback = "Yes"
        else:
            oneback = "No"
            rand = random.randint(1,3)
            if rand == 1:
                #first, check that face count hasn't maxed out
                if faces_shown >= 90:
                    continue
                #show a face
                stim_type = "Face"
                to_display = faces[faces_shown]
                faces_shown += 1
                #set trigger value
                trig_val = 32
            elif rand == 2:
                #first, check that object count hasn't maxed out
                if objects_shown >= 45:
                    continue
                #show an object
                stim_type = "Object"
                to_display = objects[objects_shown]
                objects_shown += 1
                #set trigger value
                trig_val = 64
            else:
                #first, check that scene count hasn't maxed out
                if scenes_shown >= 45:
                    continue
                #show a scene
                stim_type = "Scene"
                to_display = scenes[scenes_shown]
                scenes_shown += 1
                #set trigger value
                trig_val = 128
                
        #whichever image was chosen, display it
        display = visual.ImageStim(win=mywin, image=to_display, units="pix", size=250) 
        display.draw()
        #trigger the parport
        pport.Out32(pport_addr, trig_val)
        stim_start = time.time()
        stim_onset = time.time() - exp_start_time
        mywin.flip()
        #reset trigger value
        pport.Out32(pport_addr, 0)
        #display image for 500ms
        core.wait(0.5)
        
        #get timing information
        stim_end = time.time()
        stim_dur = stim_end - stim_start
        fix_start = time.time()
        fix_onset = time.time() - exp_start_time
        
        #draw fixation
        fixation.draw()
        mywin.flip()
        
        #get reaction time
        timeBefore = time.time()
        presses = event.waitKeys(1.0)
        timeAfter = time.time()
        trial_rt = timeAfter - timeBefore
        
        if(presses and presses[0] == "space" and oneback_matrix[total_shown] == 1):
            #correct response, handle 
            #print "Correct!"
            correct = "Y"
        elif(((presses and presses[0] != "space") or (not presses)) and oneback_matrix[total_shown] == 1):
            #incorrect response, handle
            #print "Incorrect response"
            correct = "N"
        else:
            correct = "n/a"
        #if not a one-back condition, save the most recently-displayed
        #image, and increment the total per-block distinct stim counter
        if oneback_matrix[total_shown] == 0:
            last_shown = to_display
            stims_shown += 1
        #increment total stim counter
        total_shown += 1
            
        #wait out the remaining time
        core.wait(1.0 - trial_rt)
        
        #get timing information
        end_fix = time.time()
        fix_dur = end_fix - fix_start
        
        #break every 25 trials
        if (total_shown + 1) % 25 == 0:
            break_fix.draw()
            mywin.flip()
            presses = event.waitKeys()
            fixation.draw()
            mywin.flip()
            core.wait(2.0)
            
        datafile.write("{}\t{}\t{}\t\t{}\t\t{}\t\t{}\t{}\t{}\t{}\t{}\n".format(cur_block, \
                                                                   total_shown, \
                                                                   stim_type, \
                                                                   oneback, \
                                                                   correct, \
                                                                   trial_rt, \
                                                                   stim_onset, \
                                                                   stim_dur, \
                                                                   fix_onset, \
                                                                   fix_dur))
        datafile.flush()                                                          
    
    wait_text = visual.TextStim(win=mywin, text="You have finished this block. Press any key to continue.")
    
    presses = event.waitKeys()
    if presses:
        cur_block += 1
        continue

datafile.close()          
mywin.close()
core.quit()

