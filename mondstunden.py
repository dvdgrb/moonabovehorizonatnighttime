# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 21:17:50 2021

@author: DGruber
"""

import math
import datetime
import matplotlib.pyplot as plt

import astropy.units as u
from astroplan import Observer
from astropy.time import Time


#define observer at given location 
obs = Observer(longitude=11.343*u.deg, latitude=46.505*u.deg, elevation=225*u.m, name="OBSERVER")

#define start time
time = Time('2021-01-01 00:00:00')
    
#create empty arrays which will be populated later in while loop    
hours= []
phase = []
dates = []
   
#while we are still in 2021 do the following
while time < Time('2022-01-01 00:00:00'):
    #"moon visibility clock"; accumulates number of hours when the moon is visible/above horizon and it is night time
    clock = 0
    
    #create a second instance of time
    time2 = time
    
    #while we are still within the fiven day do the following
    while time2 < time+datetime.timedelta(days=1):
        #check whether moon is above horizon and whether it is nighttime
        if obs.is_night(time2) and obs.moon_altaz(time2).alt >= 0: 
            #if so, add 0.1 hours to the "moon visibility clock"
            clock = clock + 0.1
        #increment time with 0.1 hours and re-check above condition           
        time2 = time2 + datetime.timedelta(hours=0.1)
    
    #add hours for the given day to the array
    hours.append(clock)
    #add phase to array, where phase = 0 --> full moon, phase = 1 --> new
    phase.append((obs.moon_phase(time2)/(math.pi)).value)
    #add date which was checked
    dates.append(time) 
    
    #printout to check advancement of script
    print("{0.iso}".format(time), clock, obs.moon_phase(time2)/(math.pi))
    
    #reset clock for the next day to check
    clock = 0
    
    #jump to the next day which needs to be checked
    time = time + datetime.timedelta(days=1)

#plot everything    
plt.plot(phase, hours, 'bo', markersize=1)
plt.ylabel("Moon above horizon while Sun is down [h]")
plt.xlabel("Moon phase [1 = new, 0 = full]")
plt.show