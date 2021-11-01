# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 13:33:53 2021

@author: tcunn
"""
import random

class Agent():
    def __init__(self, environment):
        self._x = random.randint(0, len(environment[0]))
        self._y = random.randint(0, len(environment))
        self.environment = environment
        self.store = 0    
    
    def __str__(self):
        return "x: " + str(self.x) + "\n" + \
            "y: " + str(self.y) + "\n" + \
            "store: " + str(self.store)
    
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
            self._x = (self._x + 1) % len(self.environment[0])
        else:
            self._x = (self._x - 1) % len(self.environment[0])
        
        if random.random() < 0.5:
            self._y = (self._y + 1) % len(self.environment)
        else:
            self._y = (self._y - 1) % len(self.environment)
    
    def eat(self):
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        elif self.environment[self.y][self.x] > 0:
            self.store = self.environment[self.y][self.x]
            self.environment[self.y][self.x] = 0
        
        # Make agent throw up store if eaten over 100 units
        if self.store > 100:
            self.environment[self.y][self.x] += self.store
            self.store = 0
            
    x = property(get_x, set_x, "x property")
    y = property(get_y, set_y, "y property")
    
        
       
