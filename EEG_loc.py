# -*- coding: utf-8 -*-
"""
Written on Thurs Dec 1 2016

@author Austin Marcus - aimarcus@andrew.cmu.edu
Localizer - one-back faces, objects, scenes
500ms stim pres time, 1s ITI
"""

from psychopy import visual, core, event
import time

#create a window
mywin = visual.Window([1000, 1000], winType="pyglet", screen="1", units="deg")

#create some stimuli
grating = visual.GratingStim(win=mywin, mask="circle", size=3, pos=[-4,0], sf=3)
fixation = visual.GratingStim(win=mywin, size=0.5, pos=[0,0], sf=0, rgb=-1)

#draw the stimuli and update the window
grating.draw()
fixation.draw()
mywin.update()

#pause, so you get a chance to see it!
core.wait(5.0)
