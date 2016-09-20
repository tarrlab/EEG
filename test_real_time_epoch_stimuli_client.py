# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 17:34:38 2016
Modified from the mne realtime example
@author: Ying Yang
@author: Austin Marcus
"""


from psychopy import visual
import sys
paths = ['C:\\ExperimentData\\YingYang\\tools\\mne-python-master\\']
for path0 in paths:
    sys.path.insert(0,path0)

from mne.realtime import StimClient
from psychopy import core
from ctypes import windll


# create a port object to use in the session
pport = windll.inpoutx64

# try psychopy's parallel class concurrently
# pyport = parallel.ParallelPort(0xcff8)

# create a window
mywin = visual.Window([800, 600], monitor="testMonitor", units="deg")
 
# create the stimuli
 
# right checkerboard stimuli
right_cb = visual.RadialStim(mywin, tex='sqrXsqr', color=1, size=5,
                             visibleWedge=[0, 180], radialCycles=4,
                             angularCycles=8, interpolate=False,
                             autoLog=False)
 
# left checkerboard stimuli
left_cb = visual.RadialStim(mywin, tex='sqrXsqr', color=1, size=5,
                            visibleWedge=[180, 360], radialCycles=4,
                            angularCycles=8, interpolate=False,
                            autoLog=False)
 
# fixation dot
fixation = visual.PatchStim(mywin, color=-1, colorSpace='rgb', tex=None,
                            mask='circle', size=0.2)
 
# the most accurate method is using frame refresh periods
# however, since the actual refresh rate is not known
# we use the Clock
timer1 = core.Clock()
timer2 = core.Clock()

#setting parallel port value
#parallel.setPortAddress(<port_address>)
  
# Instantiating stimulation client
 
# Port number must match port number used to instantiate
# StimServer. Any port number above 1000 should be fine
# because they do not require root permission.
stim_client = StimClient('localhost', port=4218)
#for i in range(200):
#    print stim_client.get_trigger(timeout=0.2)

#stim_client.close()

# There is socket time out error, I don't know why

fixation.draw()  # draw fixation
mywin.flip()  # show fixation dot

timer1.reset()  # reset timer
timer1.add(5)  # display stimuli for 0.75 sec

'''
mywin.close()  # close the window
#core.quit()
'''


 
#ev_list = list()  # list of events displayed
ev_list = [100, 200, 100, 200]
# start with right checkerboard stimuli. This is required
# because the ev_list.append(ev_list[-1]) will not work
# if ev_list is empty.
trig = 100

# iterating over 50 epochs
for ii in range(10):
    pport.Out32(0xcff8, 0)  # set trigger pins to low
 
    if trig is not None:
        ev_list.append(trig)  # use the last trigger received
    else:
        ev_list.append(ev_list[-1])  # use the last stimuli
 
    # draw left or right checkerboard according to ev_list
 
    # pyport.setData(255) # set parport pins all high
    pport.Out32(0xcff8, 255)    # set parport pins all high    
    
    if ev_list[ii] == 200:
        left_cb.draw()
    else:
        right_cb.draw()
        
    pport.Out32(0xcff8, 0)  # set parport pins all low
    # pyport.setData(0)   # set parport pins all low
 
    fixation.draw()  # draw fixation
    mywin.flip()  # show the stimuli
 
    timer1.reset()  # reset timer
    timer1.add(0.75)  # display stimuli for 0.75 sec
 
    # return within 0.2 seconds (< 0.75 seconds) to ensure good timing
    trig = stim_client.get_trigger(timeout=0.2)
    
    print "got the trigger"
    
    pport.Out32(0xcff8, 255)
 
    # wait till 0.75 sec elapses
    while timer1.getTime() < 0:
        pass
    
    fixation.draw()  # draw fixation
    mywin.flip()  # show fixation dot
 
    timer2.reset()  # reset timer
    timer2.add(0.25)  # display stimuli for 0.25 sec
 
    # display fixation cross for 0.25 seconds
    while timer2.getTime() < 0:
        pass
    print "hello"
mywin.close()  # close the window
core.quit()
