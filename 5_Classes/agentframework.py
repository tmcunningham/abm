# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 13:33:53 2021

@author: tcunn
"""
import random

class Agent():
    def __init__(self):
        self._x = random.randint(0, 99)
        self._y = random.randint(0, 99)
    
    def get_x(self):
        return self._x
    
    def set_x(self, value):
        self._x = value
        
    def get_y(self):
        return self._y
    
    def set_y(self, value):
        self._y = value
    
    def move(self):
        if random.random() < 0.5:
            self._x = (self._x + 1) % 100
        else:
            self._x = (self._x - 1) % 100
        
        if random.random() < 0.5:
            self._y = (self._y + 1) % 100
        else:
            self._y = (self._y - 1) % 100
    
    x = property(get_x, set_x, "x property")
    y = property(get_y, set_y, "y property")
    
        
       
