# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 13:33:53 2021

@author: Tom Cunningham
"""
import random
import operator

class Agent():
    """
    Define an instance of a single agent.
    
    Properties
    ----------
    x : int 
        Agent's x co-ordinate.
    y : int
        Agent's y co-ordinate.
    environment : list
        Raster data of environment.
    store : int 
        Amount of food the agent currently has in its stomach.
    agents : list
        All agents in environment.
    id : list
        Agent's id number.
    speed : int
        How many spaces the agent will move in a single movement.
               
    Methods
    -------
    move()
        Moves agent in y direction (up or down at random) and in x direction 
        (left or right at random).
    
    distance_between(other_agent)
        Calculates Euclidean distance between this agent and another agent.
    """
    def __init__(self, id, speed, environment, agents,
                 x = None, y = None):
        """
        Constructor function for agent.
        
        Parameters
        ----------
        id : int 
            Agent's id number.
        speed : int
            How many spaces the agent will move in a single movement.
        environment : list
            Raster data of environment.
        agents : list
            All agents in environment.
        x : int
            Agent's x co-ordinate. Defaults to None. If None, set as random x 
            co-ordinate within the environment.
        y : int
            Agent's y co-ordinate. Defaults to None. If None, set as random y 
            co-ordinate within the environment.
        """
        if x == None:
            self._x = random.randint(0, len(environment[0]) - 1)
        else:
            self._x = x
            
        if y == None:
            self._y = random.randint(0, len(environment) - 1)
        else:
            self._y = y
            
        self.environment = environment
        self.store = 0 
        self.agents = agents
        self.id = id
        self.speed = speed
    
    def __str__(self):
        """
        Print the id, x and y co-ordinates and the current store of the agent.
        """
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
        """
        Move agent in x direction and y direction (i.e. diagonally).
        
        Whether x and y co-ordinates are increased or decreased is decided at
        random. The amount the agent moves is equal to its speed.
        """
        if random.random() < 0.5:
            self._x = (self._x + self.speed) % len(self.environment[0])
        else:
            self._x = (self._x - self.speed) % len(self.environment[0])
        
        if random.random() < 0.5:
            self._y = (self._y + self.speed) % len(self.environment)
        else:
            self._y = (self._y - self.speed) % len(self.environment)
    
    def distance_between(self, other_agent):
        """
        Measure Euclidean distance between this agent and another agent.
        
        Parameters
        ----------
        other_agent : agent
            The agent to measure the distance from.
        """
        return ((self.x - other_agent.x)**2 + (self.y - other_agent.y)**2)**0.5
             
    x = property(get_x, set_x, "x property")
    y = property(get_y, set_y, "y property")

class Sheep(Agent):
    """
    Define an instance of a single sheep. Inherits Agent class.
    
    Methods
    -------
    eat()
        Increase store by 10 and remove 10 units from environment at sheep's 
        current co-ordinate.
    
    throw_up()
        If store is over 100, add store amount to the environment at sheep's
        current co-ordinate and set store to 0.
    
    share_with_neighbours(neighbourhood)
        If there is an agent within the neighbourhood of this agent with a 
        lower store, split the total store between the two agents.
        
    """
    def eat(self):
        """
        Increase store by 10 and remove 10 units from environment at sheep's 
        current co-ordinate.
        
        If there are fewer than 10 units remaining in the environment at the
        surrent position, add the remaining number of units to store and set
        the environment value to be 0.
        """
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
        elif self.environment[self.y][self.x] > 0:
            self.store = self.environment[self.y][self.x]
            self.environment[self.y][self.x] = 0
        
    def throw_up(self):
        """
        If store is over 100, add store amount to the environment at sheep's
        current co-ordinate and set store to 0.
        """
        if self.store > 100:
            self.environment[self.y][self.x] += self.store
            self.store = 0   
    
    def share_with_neighbours(self, neighbourhood):
        """
        share_with_neighbours(neighbourhood)
            If there is an agent within the neighbourhood of this sheep with a 
            lower store, split the total store between the two agents.
            
            This is done by looping over agents, giving priority to those
            earlier in the list of agents. This method calls distance_between
            from the agent superclass.
            
            Parameters
            ----------
            neighbourhood : int
                The distance within which to look for another agent.
        """
        # print(neighbourhood) # Check the method works
        # Loop through the agents in self.agents
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
    """
    Define an instance of a single wolf. Inherits Agent class.
    
    Methods
    -------
    eat(neighbourhood)
        If there is a sheep within the neighbourhood of this wolf, remove the 
        sheep from the list of agents and add one to the wolf's store.
    """
    def eat(self, neighbourhood):
        """
        If there is a sheep within the neighbourhood of this wolf, remove the 
        sheep from the list of agents and add one to the wolf's store.
        
        Will also print out a message that a sheep has been eaten and give the
        sheep's details. This method inherits the __str__ and distance_between
        methods from the agent superclass.
        
        Parameters
        ----------
        neighbourhood : int
            The distance within which to look for a sheep.
        """
        distances = []
        sheeps = [agent for agent in self.agents if isinstance(agent, Sheep)]
        
        if len(sheeps) > 0:
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

    
       
