# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 17:39:20 2016

@author: Ying Yang, yingyan1@andrew.cmu.edu
"""
import sys
paths = ['C:\\ExperimentData\\YingYang\\tools\\mne-python-master\\',
         'C:\\FieldTrip\\fieldtrip-20160810\\realtime\\src\\buffer\\python\\'
         'C:\\ExperimentData\\YingYang\\Real_time\\Initial_test_script\\']
for path0 in paths:
    sys.path.insert(0,path0)    
from real_time_epoch_from_fieldtrip_biosemi_buffer import biosemi_fieldtrip_recent_epochs

import numpy as np
import matplotlib.pyplot as plt
import mne
from mne.realtime import FieldTripClient
import time
from mne.realtime import StimServer


# debug
'''
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

# ===debugging===
rt_client = FieldTripClient(info = None, host = "localhost", port = 1972, 
                            tmax = 150, wait_max = 10)
rt_client.__enter__()

pport.Out32(0xcff8, 0)  # set trigger pins to low
    
# testing: tie trigger value to trigger sent from server session
trig_seq = [100, 200, 100, 100, 200]    
    
for i in range(len(trig_seq)):
    trig = trig_seq[i]
    pport.Out32(0xcff8, 0)  # set parport pins all low
    time.sleep(1)
    pport.Out32(0xcff8, trig)    
    time.sleep(0.1)
    
    pport.Out32(0xcff8, 0)  # set parport pins all low
    time.sleep(1)
    
    
ftc = rt_client.ft_client
event_list = list(ftc.getEvents())
#for e in event_list[::-1]:
#    print e
    
H = ftc.getHeader()    
current_nSamples = H.nSamples
event_types = [100, 200]
for e in event_list[::-1]:
    # get event type and event sample
    str_e =(str(e)).replace(":","\n").replace('[',' ').replace(']',' ').split()
    # hard coded: split at n, type, trigger, value, [100], Sample, 470968, Offset, 0, Duration, 0
    current_event_ind = int(str_e[5])
    current_event_type = float(str_e[3]) # '[100]'
    if current_event_type in event_types:
        print (current_event_ind,current_event_type)

                

#recent_epochs_obj = biosemi_fieldtrip_recent_epochs(rt_client, n_recent_event = 1)
#recent_epochs, recent_event_list = recent_epochs_obj.get_recent_epochs()

'''
#=========================

                     
with FieldTripClient(host='localhost', port=1972,
		             tmax=150, wait_max=10) as rt_client:
    recent_epochs_obj = biosemi_fieldtrip_recent_epochs(rt_client, n_recent_event = 1,
                                                        event_types = [100, 200])
    
    with StimServer(port=4218) as stim_server:
            
        # send a testing trigger
        stim_server.start(verbose=True)
        # Just some initially decided events to be simulated
        # Rest will decided on the fly
        #ev_list = np.tile(np.array([100,200]),[5,1]).ravel()
        #for ii in range(len(ev_list)):
            # Tell the stim_client about the next stimuli
            #time.sleep(1)
            #stim_server.add_trigger(ev_list[ii])
            # Collecting data
        
        first_ev = 100
        time.sleep(1)
        stim_server.add_trigger(first_ev)
        
        time.sleep(1)        
        recent_epochs, recent_event_list = recent_epochs_obj.get_recent_epochs()
        print recent_event_list
        
        # check recent_event_list for trigger type to determine next stim - see if 
        # triggers are getting properly read in from FieldTrip buffer
        for ii in range(0,9):
            time.sleep(1)
            if recent_event_list[-1][1] == 100.0:
                next_ev = 200
            else:
                next_ev = 100
            stim_server.add_trigger(next_ev)
            recent_epochs, recent_event_list = recent_epochs_obj.get_recent_epochs()
            print 'DEBUG~~contents of buffer list: {}'.format(recent_event_list[-1][1])
                
        recent_epochs.resample(512.0)
        recent_epochs.apply_baseline((None,0))
        
        # test to avoid socket timeout error
        time.sleep(1)
    
    
   