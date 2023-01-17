#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 18:07:54 2022

@author: BedenPag
"""

import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from random import random


mydata= pd.read_excel('C:/Users/HOM-0317-TB01/Documents/GitHub/MDM3phaseB/PlainData.xlsx')

# Constants for bed data
beds = 300
aLOS = 15
# Collect the length of stay data
LOS = mydata.iloc[:,1]
# Create a normal distribution of the length of stay data with a mean of aLOS
nLOS = np.random.normal(aLOS, LOS.std(), beds)


illness = ['Myocardial Infarction','Stroke','COVID 19', 'Fracture of Femur', 'Atrial Fibrilation', 'Pneumonia', 'Endocrine, Nutritional and Metabolic Diseases', 'COPD']
means = [6.9,28.2,15.95,30.55,4.25,14.9,3.5,7.05]
data = []
# Append a exponential distribution of the means to the data list
for i in means:
    data.append(np.random.exponential(i, beds))

# Create a dictionary of the illness and the data
illnessData = dict(zip(illness, data))


# Plot each illness as a probability density function
#for i in illnessData:
#    plt.hist(illnessData[i], density=True, bins=int(max(illnessData[i])))
#    plt.title(i)
#    plt.xlabel('Days')
#    plt.ylabel('Probability')
#    plt.show()

ALLxydata = []
# Plot each illness as a cumulative probability density function
for i in illnessData:
    plt.hist(illnessData[i], density=True, cumulative=True, bins=int(max(illnessData[i])))
    plt.title(i)
    plt.xlabel('Days')
    plt.ylabel('Probability')
    # plot a line for the cumulative probability
    lineplot = plt.plot(np.sort(illnessData[i]), np.linspace(0, 1, len(illnessData[i]), endpoint=False))
    ax = plt.gca()
    line = ax.lines[0]
    xydata = line.get_xydata()
    ALLxydata.append(xydata)
    plt.show()

illnessLOSprobability = dict(zip(illness, ALLxydata))

# q: which data point is closest to 1 for each ilness in illnessLOSprobability



def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# find the first column of each illness in illnessLOSprobability


Prob = []
day = []
ProbLeave = []
iteration1 = 1
dayNum = 0
for i in illness: # for each illness
    q = illnessLOSprobability[i][:,0]
    while dayNum <= int(max(illnessData[i])): # for each day
        dayNum = dayNum + 1
        for j in q:
            nearest = find_nearest(q,why) # find the nearest value to that day
            if j == nearest: # if nearest value is found 
                prob = illnessLOSprobability[i][iteration1,1] # find the corisponding probability of leaving
                iteration1 = 0
                Prob.append(prob)
                day.append(dayNum)
                break
            iteration1 = iteration1 +1
        arr = np.stack((day, Prob), axis=1)
    ProbLeave.append(arr)
        
    why = 0

ProbDic = dict(zip(illness,ProbLeave))

# 


admission = 55
# For each admission, give them a random illness
for i in range(admission):
    # Choose a random illness
    illnessName = np.random.choice(list(illnessData.keys()))
    # Find a number of days for that illness following a probability distribution
    for i in ProbDic[illnessName][:,0]:
        j = random()
        if j < ProbDic[illnessName][int(i),1]:
            days = int(i)
            break
    # Create a dictionary of the illness and the days
    dailyAdmissions = np.stack((illnessName, days))
    print(dailyAdmissions)





