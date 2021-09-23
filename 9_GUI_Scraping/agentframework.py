# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 13:33:53 2021

@author: tcunn
"""
import random
import operator

class Agent():
    def __init__(self, id, speed, environment, agents,
                 x = None, y = None,):
        if x == None:
            self._x = random.randint(0, len(environment[0]))
        else:
            self._x = x
            
        if y == None:
            self._y = random.randint(0, len(environment[0]))
        else:
            self._y = y
            
        self.environment = environment
        self.store = 0 
        self.agents = agents
        self.id = id
        self.speed = speed
    
    def __str__(self):
        return "id: " + str(self.id) + ", " + \
            "x: " + str(self.x) + ", " + \
            "y: " + str(self.y) + ", " + \
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
            self._x = (self._x + self.speed) % len(self.environment[0])
        else:
            self._x = (self._x - self.speed) % len(self.environment[0])
        
        if random.random() < 0.5:
            self._y = (self._y + self.speed) % len(self.environment)
        else:
            self._y = (self._y - self.speed) % len(self.environment)
    
    def distance_between(self, other_agent):
        return ((self.x-other_agent.x)**2 + (self.y-other_agent.y)**2)**0.5
             
    x = property(get_x, set_x, "x property")
    y = property(get_y, set_y, "y property")

class Sheep(Agent):
    def eat(self):
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        elif self.environment[self.y][self.x] > 0:
            self.store = self.environment[self.y][self.x]
            self.environment[self.y][self.x] = 0
        
    def throw_up(self):
        if self.store > 100:
            self.environment[self.y][self.x] += self.store
            self.store = 0   
    
    def share_with_neighbours(self, neighbourhood):
        #print(neighbourhood) - check the method works
        # Loop through the agents in self.agents .
        for agent in self.agents:
            # Calculate the distance between self and the current other agent:
            distance = self.distance_between(agent)
            # If distance is less than or equal to the neighbourhood
            if distance <= neighbourhood:
                # Sum self.store and agent.store and halve to calculate average
                average_store = (self.store + agent.store)/2
                self.store = average_store
                agent.store = average_store
                
class Wolf(Agent):
    def eat(self, neighbourhood):
        distances = []
        sheeps = [agent for agent in self.agents if isinstance(agent, Sheep)]
        for sheep in sheeps:
            distances.append(self.distance_between(sheep))
        min_distance = min(enumerate(distances), key = operator.itemgetter(1))
        closest_sheep = sheeps[min_distance[0]]
        if min_distance[1] < neighbourhood:
            self.x = closest_sheep.x
            self.y = closest_sheep.y
            self.store += 1
            self.agents.remove(closest_sheep)
            print("A sheep was eaten! \n " + str(closest_sheep))

    
       
