# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 23:44:31 2021

@author: tcunn
"""

import subprocess

# Open file for total stores to be written into
f = open("total store amounts.txt", "w")

# Run through range of different number of agents and get total store amounts
for i in range(10, 110, 10):
    model = subprocess.call(["python", "model.py", 
                             str(i), "20", "30", "False"], 
                            stdout = f)
    print(model)

f.close()