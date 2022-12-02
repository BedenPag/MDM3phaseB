#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 18:07:54 2022

@author: BedenPag
"""

import math
import matplotlib.pyplot as plt
import scipy.stats as sps
import pandas as pd
import numpy as np
import seaborn as sns
sns.set(style='ticks')

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

# Plot each illness as a cumulative probability density function
for i in illnessData:
    plt.hist(illnessData[i], density=True, cumulative=True, bins=int(max(illnessData[i])))
    plt.title(i)
    plt.xlabel('Days')
    plt.ylabel('Probability')
    # plot a line for the cumulative probability
    twat = plt.plot(np.sort(illnessData[i]), np.linspace(0, 1, len(illnessData[i]), endpoint=False))
    ax = plt.gca()
    line = ax.lines[0]
    xydata = line.get_xydata()
    print(xydata)
    plt.show()
    






# for each x in the probability density function, give it its y value
#for i in illnessData:
#    for x in illnessData[i]:
#        y = (1/i)*math.exp(-x/i)
#        print(y)
#        plt.plot(x,y)
#        plt.show()



admission = 55
dailyAdmissions = []
# For each admission, give them a random illness
for i in range(admission):
    # Choose a random illness
    illnessName = np.random.choice(list(illnessData.keys()))
    # Find a number of days for that illness following a probability distribution
    days = np.random.choice(illnessData[illnessName])
    # Create a dictionary of the illness and the days
    dailyAdmissions.append({illness:days})




