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

rt_client = FieldTripClient(info = None, host = "localhost", port = 1972, 
                            tmax = 150, wait_max = 10)
with FieldTripClient(host='localhost', port=1972,
		             tmax=150, wait_max=10) as rt_client:
    recent_epochs_obj = biosemi_fieldtrip_recent_epochs(rt_client, n_recent_event = 1)
    
    with StimServer(port=4218) as stim_server:
            
        # send a testing trigger
        stim_server.start(verbose=True)
        # Just some initially decided events to be simulated
        # Rest will decided on the fly
        ev_list = np.tile(np.array([100,200]),[5,1]).ravel()
        for ii in range(len(ev_list)):
            # Tell the stim_client about the next stimuli
            time.sleep(1)
            stim_server.add_trigger(ev_list[ii])
            # Collecting data
'''
        recent_epochs, recent_event_list = recent_epochs_obj.get_recent_epochs()
        recent_epochs.resample(512.0)
        recent_epochs.apply_baseline((None,0))
'''
