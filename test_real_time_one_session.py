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
from mne.realtime import StimServer
from mne.realtime import StimClient
from mne.realtime import FieldTripClient
import time


from psychopy import visual
from psychopy import core
from ctypes import windll
import time


'''
class trigger():
    
    
    
    def __init__(self):
        self.address = 0xcff8
        self.pport = windll.inpoutx64
        self.events = [100,200]
        
    def send():
        pass        
        
        
    def reset():
        pass
        '''
        
# object wrapper for FieldTrip buffer client server session
class server():
    
    def __init__(self, session_port, rt_client, stim_server):
        print "Initializing server"
        self.session_port = session_port
        #self.rt_client = FieldTripClient(host='localhost', port=1972,
	  #	             tmax=150, wait_max=10)
        self.rt_client = rt_client
        self.recent_epochs_obj = biosemi_fieldtrip_recent_epochs(self.rt_client, n_recent_event = 1,
                                                        event_types = [100, 200])
        #self.server = StimServer(port=self.session_port)
        self.stim_server = stim_server
    
    # start running 'experiment' - control client
    def run(self):
        print "RUNNING SERVER"
        self.stim_server.start(verbose=True)
        #self.client_session = client(self.session_port, 0xcff8)
        #self.client_session.run()
        first_ev = 100
        #time.sleep(1)
        self.put_trigger(first_ev)
        
        time.sleep(15)        
        recent_epochs, recent_event_list = self.get_recent()
        print recent_event_list
        
        '''
        # check recent_event_list for trigger type to determine next stim - see if 
        # triggers are getting properly read in from FieldTrip buffer
        for ii in range(0,9):
            time.sleep(1)
            if recent_event_list[-1][1] == 100.0:
                next_ev = 200
            else:
                next_ev = 100
            self.put_trigger(next_ev)
            recent_epochs, recent_event_list = self.get_recent()
            print 'DEBUG~~contents of buffer list: {}'.format(recent_event_list[-1][1])
                
        recent_epochs.resample(512.0)
        recent_epochs.apply_baseline((None,0))
        '''
        # test to avoid socket timeout error
        time.sleep(1)
        
    # send a trigger to the presentation object
    def put_trigger(self, trig_val):
        self.stim_server.add_trigger(trig_val)
        
    # get recent epochs from FieldTrip buffer
    def get_recent(self):
        return self.recent_epochs_obj.get_recent_epochs()
        
    
# object wrapper for presentation client session
class client():
    
    def __init__(self, session_port, trig_addr):
        print "Initializing client"
        # IPC stuff
        self.session_port = session_port
        self.pport = windll.inpoutx64
        self.trig_addr = trig_addr
        self.stim_client = StimClient('localhost', port=self.session_port)
        
         # timers
        self.timer1 = core.Clock()
        self.timer2 = core.Clock()

    # run 'experiment'
    def run(self):
        print "RUNNING CLIENT"   
                
        # stimulus display stuff
        self.mywin = visual.Window([800, 600], monitor="testMonitor", units="deg")  # display window
        self.right_cb = visual.RadialStim(self.mywin, tex='sqrXsqr', color=1, size=5,
                             visibleWedge=[0, 180], radialCycles=4,
                             angularCycles=8, interpolate=False,
                             autoLog=False)                                         # right checkerboard
        self.left_cb = visual.RadialStim(self.mywin, tex='sqrXsqr', color=1, size=5,
                            visibleWedge=[180, 360], radialCycles=4,
                            angularCycles=8, interpolate=False,
                            autoLog=False)                                          # left checkerboard
        self.fixation = visual.PatchStim(self.mywin, color=-1, colorSpace='rgb', tex=None,
                            mask='circle', size=0.2)                                # fixation
        
        # events
        self.ev_list = []
        
        # start with fixation for 0.75 sec
        self.fixation.draw()
        self.mywin.flip()
        self.timer1.reset()
        self.timer1.add(0.75)
        
        trig = self.retrieve(0.2)
        print "DEBUGGING: trig = {}".format(trig)
        self.reset_trigger()
        if trig == 100:
            self.right_cb.draw()
        
        self.send_trigger(trig)
        self.mywin.flip()
        self.timer1.reset()
        self.reset_trigger()
        
        while self.timer1.getTime() < 0:
            pass
        
        self.mywin.close()
        
        '''
        # run 10 sample trials
        for ii in range(10):
            self.reset_trigger()
    
    
            # testing: tie trigger value to trigger sent from server session
            trig = self.retrieve(0.2)
            
         
            #if trig is not None:
            #    ev_list.append(trig)  # use the last trigger received
            #else:
            #    ev_list.append(ev_list[-1])  # use the last stimuli
         
            while trig is None:
                trig = self.retrieve(0.2)
              
            self.ev_list.append(trig)   
            print ev_list
         
            # draw left or right checkerboard according to ev_list
         
            # pyport.setData(255) # set parport pins all high   
            
            if self.ev_list[ii] == 200:
                self.left_cb.draw()
            else:
                self.right_cb.draw()
                
            self.reset_trigger()  # set parport pins all low
            # pyport.setData(0)   # set parport pins all low
         
            self.fixation.draw()  # draw fixation
            self.send_trigger(trig)    # set parport pins to latest trigger 
            self.mywin.flip()  # show the stimuli
         
            self.timer1.reset()  # reset timer
            self.timer1.add(0.75)  # display stimuli for 0.75 sec
         
            # return within 0.2 seconds (< 0.75 seconds) to ensure good timing
            #trig = stim_client.get_trigger(timeout=0.2)
            
            # testing trigger retrieval from server session
            #pport.Out32(0xcff8, trig)
         
            # wait till 0.75 sec elapses
            while self.timer1.getTime() < 0:
                pass
            
            self.fixation.draw()  # draw fixation
            self.mywin.flip()  # show fixation dot
         
            self.timer2.reset()  # reset timer
            self.timer2.add(0.25)  # display stimuli for 0.25 sec
         
            # display fixation cross for 0.25 seconds
            while self.timer2.getTime() < 0:
                pass
            
            time.sleep(1)
        self.mywin.close()  # close the window
        '''
    # get trigger from server session        
    def retrieve(self, time_val):
        return self.stim_client.get_trigger(timeout=time_val)
        
    # send trigger to BioSemi by setting parport bits
    def send_trigger(self, trig_val):
        self.pport.Out32(self.trig_addr, trig_val)
        
    # reset parport bits all low
    def reset_trigger(self):
        self.pport.Out32(self.trig_addr, 0)
     
'''
with FieldTripClient(host='localhost', port=1972,
		             tmax=150, wait_max=10) as rt_client:  
    with StimServer(port=4218) as stim_server:
        server_session = server(4218, rt_client, stim_server)
        server_session.run()
'''
client_session = client(4218, 0xcff8)
print "ABOUT TO RUN CLIENT MAYBE"
client_session.run()



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


#=========================
# number of trials in total
n_trial = 100                     
with FieldTripClient(host='localhost', port=1972,
		             tmax=150, wait_max=10) as rt_client:
    recent_epochs_obj = biosemi_fieldtrip_recent_epochs(rt_client, n_recent_event = 1,
                                                        event_types = [100, 200])
    
    
            
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
    
  '''  
   