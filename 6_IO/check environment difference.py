# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 11:49:47 2021

@author: tcunn
"""

import csv

new_environment = []        
with open('out.txt', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        rowlist = []
        for value in row: 
            rowlist.append(value)
        new_environment.append(rowlist)     
        
old_environment = []

# Read in CSV raster data
with open('in.txt', newline='') as f:
    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        rowlist = []
        for value in row: 
            rowlist.append(value)
        old_environment.append(rowlist)
    

def diff(lis1, lis2):
    for i, (x, y) in enumerate(zip(lis1, lis2)):
        for j, (x1, y1) in enumerate(zip(x, y)):
            if x1 != y1:
                yield i, j


print(list(diff(new_environment, old_environment)))

print(old_environment[0][162])
print(new_environment[0][162])