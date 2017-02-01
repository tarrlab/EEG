# EEG

Master repository for all Tarrlab EEG code.

## EEG_RealTime
Code for real-time closed-loop EEG data acquisition, analysis, &amp; dynamic stimulus presentation
Primary author: Ying Yang (yingyan1@andrew.cmu.edu)
Secondary contributor: Austin Marcus (aimarcus@andrew.cmu.edu)

*Developed for use on 64-bit Windows 7 on a System76 machine with Python 2.7, FieldTrip's biosemi2ft acquisition tool, PsychoPy, MNE-Python, and Anaconda, in conjunction with the BioSemi 128-channel EEG recording system using the ActiveTwo AD-Box and AIB box with a USB2 reciever connected to a 32-bit parallel port as found in the EEG Lab at the Department of Psychology, Carnegie Mellon University, Pittsburgh PA. Use of 32-bit parallel port on a 64-bit system requires installation of a 32-bit port driver interface; [inpout32](http://www.highrez.co.uk/downloads/inpout32/) was used on our system and included in the Windows DLL search path.*

###test_real_time_one_session.py
Wraps session into one object. FieldTrip buffer client is stored as a field, and trigger values are read in real-time to control the display of a simple checkerboard experiment (alternate based on last trigger sent).
Working as of 10/13/2016

This toolbox is licensed under the GNU GPL, and any components adapted from existing packages are used, adapted and/or distributed as per the end-user license terms of each package (see LICENSE.md).

### @to_include: filenames, descriptions, relationships between them & functions!

(uploaded 9/20/2016 by Austin Marcus)
(recent update: 10/13/2016 by Austin Marcus)

## [Kevin Tan's EEGLAB Pipeline](https://github.com/kevmtan/EEGpipeline/wiki)

Kevin Tan's EEGLAB pipeline performs ICA-based EEG preprocessing and source localization

A detailed practical, algorithmic and theoretical overview of this pipeline can be found here: https://github.com/kevmtan/EEGpipeline/wiki

Read the above wiki before using this pipeline
