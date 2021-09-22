# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:33:27 2021

@author: tcunn
"""
import random

# Create random starting x0 and y0 for a 100x100 grid.
y0 = random.randint(0, 99)
x0 = random.randint(0, 99)

# Change y0 and x0 twice based on random numbers.
if random.random() < 0.5:
    y0 += 1
else:
    y0 -= 1

if random.random() < 0.5:
    x0 += 1
else:
    x0 -= 1

if random.random() < 0.5:
    y0 += 1
else:
    y0 -= 1

if random.random() < 0.5:
    x0 += 1
else:
    x0 -= 1
    
print(y0, x0)

# Create random starting x1 and y1 for a 100x100 grid.
y1 = random.randint(0, 99)
x1 = random.randint(0, 99)

# Change x1 and y1 twice based on random numbers.
if random.random() < 0.5:
    y1 += 1
else:
    y1 -= 1

if random.random() < 0.5:
    x1 += 1
else:
    x1 -= 1

if random.random() < 0.5:
    y1 += 1
else:
    y1 -= 1

if random.random() < 0.5:
    x1 += 1
else:
    x1 -= 1
    
print(y1, x1)

# Work out the distance between the two sets of y and xs.
distance = ((y1-y0)**2 + (x1-x0)**2)**0.5
print(distance)
