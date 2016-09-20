# -*- coding: utf-8 -*-
# Author Ying Yang,  yingyan1@andrew.cmu.edu
# implement the an MNE-rtEpoch-type object for the fieldtrip biosemi buffer 
# I need to rewrite many parts in mne-python fieldtrip client, and RtEpochs to make it work. 
# To be continued

# Fieldtrip buffer: multithresd C/C++, can be cleaned (flushed) 
# ring buffer: after a time, old data samples and events will not be accessible anymore
# http://www.fieldtriptoolbox.org/development/realtime/buffer_protocol
# In the buffer:  head structure, data matrix, a list of event structures
# 

#============ specific to the EEG aquisition machine
import sys
paths = ['C:\\ExperimentData\\YingYang\\tools\\mne-python-master\\',
         'C:\\FieldTrip\\fieldtrip-20160810\\realtime\\src\\buffer\\python\\']
for path0 in paths:
    sys.path.insert(0,path0)

import numpy as np
import matplotlib.pyplot as plt
import mne
from mne.realtime import FieldTripClient
import time


class biosemi_fieldtrip_recent_epochs:
    def __init__(self,rt_client, n_recent_event = 1, trial_tmin = 0.2, 
                  trial_tmax = 1.0, event_types = [100]):
        self.rt_client = rt_client
        self.trial_tmin = trial_tmin
        self.tiral_tmax = trial_tmax
        self.n_recent_event = n_recent_event
        self.event_types = event_types
        
        self.raw_info = self.rt_client.get_measurement_info()
        sampling_rate = self.raw_info['sfreq']
        self.time_step = 1.0/sampling_rate
        # number of samples after the stimulus onset
        self.n_sample_per_trial_pos = np.int(trial_tmax/self.time_step)
        # number of samples before onset
        self.n_sample_per_trial_neg = np.int(trial_tmin/self.time_step)
        self.trial_tmin = -self.time_step*self.n_sample_per_trial_neg
        self.trial_tmax = self.time_step*self.n_sample_per_trial_pos
        self.n_time = np.int(self.n_sample_per_trial_pos + self.n_sample_per_trial_neg+1)
        self.n_channel = len(self.raw_info['chs'])

    
    def get_recent_epochs(self):
        ftc = self.rt_client.ft_client
        # get the latest n events, n = n_recent_event
        H = ftc.getHeader()
        if H is None:
            raise ValueError('Failed to retrieve header!')
        # find the events
        recent_event_counter = 0
        event_list = list(ftc.getEvents())
        recent_event_list = []
        current_nSamples = H.nSamples
        for e in event_list[::-1]:
            # get event type and event sample
            str_e =(str(e)).replace(":","\n").replace('[',' ').replace(']',' ').split()
            # hard coded: split at n, type, trigger, value, [100], Sample, 470968, Offset, 0, Duration, 0
            current_event_ind = int(str_e[5])
            current_event_type = float(str_e[3]) # '[100]'
            if (current_event_type in self.event_types and 
             current_event_ind+self.n_sample_per_trial_pos <= current_nSamples):
                recent_event_list.append((current_event_ind,current_event_type))
                recent_event_counter+= 1
                
            if recent_event_counter >= self.n_recent_event:
                break
        
        if len(recent_event_list) == 0:
            print "no recent event found"
            return None, recent_event_list
            
        # create epochs using the data
        recent_data = np.zeros([recent_event_counter, self.n_channel, self.n_time])
        recent_event_list = recent_event_list[::-1]
        # recent_event_list was the reverse order, now reverse it again
        for ind, (current_event_ind, current_event_type) in enumerate(recent_event_list):
            recent_data[ind] = np.array(ftc.getData([np.int(current_event_ind-self.n_sample_per_trial_neg),
		                current_event_ind+self.n_sample_per_trial_pos])).T
                  
        recent_epochs = mne.EpochsArray(recent_data, self.raw_info, 
		    tmin = self.trial_tmin, baseline = None, proj = False)
	
	return recent_epochs, recent_event_list






if __name__=="__main__":
    # test 
    rt_client = FieldTripClient(info = None, host = "localhost", port = 1972, 
                            tmax = 150, wait_max = 10)
    with FieldTripClient(host='localhost', port=1972,
		             tmax=150, wait_max=10) as rt_client:
        recent_epochs_obj = biosemi_fieldtrip_recent_epochs(rt_client)
        recent_epochs, recent_event_list = recent_epochs_obj.get_recent_epochs()
        recent_epochs.resample(512.0)
        recent_epochs.apply_baseline((None,0))

