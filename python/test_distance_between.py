# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 16:33:13 2021

@author: tcunn
"""

import agentframework
import csv

# Create empty list for environment raster data
environment = []

# Read in CSV raster data
with open('in.txt', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        rowlist = []
        for value in row: 
            rowlist.append(value)
        environment.append(rowlist)

# Create 2 sheeps with co-ordinates that will test the wrap-around calculation
# of distance_between method
sheeps = []
coords = [50, 250]

# Set y to coords to be 0 to make results easier to check
for i in [0,1]:
    sheeps.append(
        agentframework.Sheep(id = i, x = coords[i], y = 0,
                             environment = environment,
                             agents = sheeps, speed = 1)
        )

# Distance between sheeps should be 100 if calculation works correctly
# Will be 200 if not taking into account the wrap-around correctly
if sheeps[0].distance_between(sheeps[1]) == 100 and \
    sheeps[1].distance_between(sheeps[0]) == 100:
        print("x coordinate calculation successful")
else:
    print("x coordinate calculation unsuccessful")

# Set x coords to be 0 to test calculation for y co-ordinates
for i in [2,3]:
    sheeps.append(
        agentframework.Sheep(id = i, x = 0, y = coords[i-2],
                             environment = environment,
                             agents = sheeps, speed = 1)
        )
    
# Distance between sheeps should be 100 if calculation works correctly
# Will be 200 if not taking into account the wrap-around correctly
if sheeps[2].distance_between(sheeps[3]) == 100 and \
    sheeps[3].distance_between(sheeps[2]) == 100:
        print("y coordinate calculation successful")
else:
    print("y calculation unsuccessful")
    