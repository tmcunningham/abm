# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:33:27 2021

@author: tcunn
"""
import matplotlib.pyplot
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

# Plot environment data
matplotlib.pyplot.imshow(environment)
matplotlib.pyplot.show()

# Create function to measure distance between two points
def distance_between(agents_row_a, agents_row_b):
    return ((agents_row_a.x-agents_row_b.x)**2 + 
            (agents_row_a.y-agents_row_b.y)**2)**0.5

# Set number of agents and number of random movements
num_of_agents = 10
num_of_moves = 100

# Create empty list for co-ords.
agents = []

# Create agents.
for i in range(num_of_agents):
    agents.append(agentframework.Agent(environment))

# Move agents.
for j in range(num_of_moves):
    for i in range(num_of_agents):
        agents[i].move()
        agents[i].eat()

# Create empty list to capture distance measurements
all_distances = []

# Calculate distance between all pairs of agents excluding themselves
for i in range(len(agents)-1):
    distances_from_agent_i = []
    for j in range(len(agents)):
        if j > i:
            distances_from_agent_i.append(distance_between(agents[i], 
                                                           agents[j]))
    all_distances.append(distances_from_agent_i)

# Plot the agents
matplotlib.pyplot.imshow(environment)
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
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

