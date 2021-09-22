# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:33:27 2021

@author: tcunn
"""
import matplotlib.pyplot
import agentframework
import csv
import random

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

# Set number of agents and number, random movements and size of neighbourhood
num_of_agents = 10
num_of_moves = 100
neighbourhood = 20

# Create empty list for agents
agents = []


fig = matplotlib.pyplot.figure(figsize = (7,7))
ax = fig.add_axes([0, 0, 1, 1])

# Create agents
for i in range(num_of_agents):
    agents.append(agentframework.Agent(environment, agents))

# Create stopping condition for animation
carry_on = True

# Define update function for animation
def update(frame_number):
      
    global carry_on
    fig.clear()
    
    # Move agents.
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()
        agents[i].share_with_neighbours(neighbourhood)    
    
    # Plot agents
    matplotlib.pyplot.imshow(environment)
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
    
    # Create list of all agents stores
    #stores = [int(agent.store) for agent in agents]
    #print(stores)
    
    # Update stopping condition if all agents have oer 70 store
    if (all(i > 70 for i in [agent.store for agent in agents])):
        carry_on = False
        print("stopping condition - all agents have over 70 store")
        

# Stop animation before max number of moves or if stopping condition met
def gen_function():
    global carry_on
    i = 0
    while (i < num_of_moves) & (carry_on):
        yield i
        i += 1

# Animate plot of agents on environment
animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, 
                                               repeat = False, 
                                               frames = gen_function())    
matplotlib.pyplot.show()

# Write new environment
with open("out.txt", "w", newline = "") as f2:
    writer = csv.writer(f2, delimiter = ",")
    for row in environment:
        writer.writerow(row)

# Get list of agents current stores
agent_stores = []
for agent in agents:
    agent_stores.append(agent.store)

# Write agents current stores to a file
with open("agent stores.txt", "a", newline = "") as f3:
    writer = csv.writer(f3, delimiter = ",")
    writer.writerow(agent_stores)

# Check agent creation is including other agents
# print(agents[0].agents[1].x, agents[1].x, agents[0].x)
