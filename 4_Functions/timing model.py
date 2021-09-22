# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:33:27 2021

@author: tcunn
"""
import random
import matplotlib.pyplot
import time

# Create empty lists to capture time taken and number of agents
times = []
agent_counts = []

for num_of_agents in (1000, 2000, 5000, 7500, 10000):
    # Start timer.
    start = time.perf_counter()
    
    def distance_between(agents_row_a, agents_row_b):
        """Measure distance between two points."""
        return ((agents_row_a[0]-agents_row_b[0])**2 + 
                (agents_row_a[1]-agents_row_b[1])**2)**0.5
    
    # Set number of random movements
    num_of_moves = 100
    
    # Create empty list for co-ords.
    agents = []
    
    # Create random starting co-ords for a 100x100 grid.
    for i in range(num_of_agents):
        agents.append([random.randint(0, 99),
                       random.randint(0, 99)])
    
    # Change starting co-ords twice based on random numbers.
    for j in range(num_of_moves):
        for i in range(num_of_agents):
            for k in (0,1):
                if random.random() < 0.5:
                    agents[i][k] = (agents[i][k] + 1) % 100
                else:
                    agents[i][k] = (agents[i][k] - 1) % 100
    
    # Work out the distance between the two sets of co-ords.
    distance = distance_between(agents[0], agents[1])
    print(distance)
    
    # Create empty list to capture distance measurements
    all_distances = []
    
    # Calculate distance between all pairs of agents excluding themselves
    for i in range(len(agents)-1):
        distances_from_agent_i = []
        for j in range(len(agents)):
            if j > i:
                distances_from_agent_i.append(distance_between(agents[i], agents[j]))
        all_distances.append(distances_from_agent_i)
    
    # Print the overall maximum and minimum pairwise distances between agents
    print("max distance = " + str(max(max(all_distances, key=max))))
    print("min distance = " + str(min(min(all_distances, key=min))))
    
    # Plot the agents
    matplotlib.pyplot.ylim(0, 99)
    matplotlib.pyplot.xlim(0, 99)
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i][1],agents[i][0])
    matplotlib.pyplot.show()
    
    # End timer.
    end = time.perf_counter()
    
    # Add time to list of times and num of agents to list of agent counts
    times.append(end - start)
    agent_counts.append(num_of_agents)
 

# Plot the times
matplotlib.pyplot.plot(agent_counts, times, color = "blue")
matplotlib.pyplot.show()
