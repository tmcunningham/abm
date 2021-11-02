# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 12:33:27 2021

@author: Tom Cunningham
"""

# Set backend for matplotlib
import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot
import matplotlib.animation
import agentframework
import csv
import random
import tkinter
import requests
import bs4
import sys

# Get data for sheep xs and ys
r = requests.get("https://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html")

# Check response is 200
# print(r)

# Parse HTML and read ys and xs
soup = bs4.BeautifulSoup(r.text, "html.parser")
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})

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

# Set number of sheep, wolves, random movements and size of neighbourhood
# Use arguments given or use defaults if not all arguments provided as ints
try:
    num_of_sheeps = int(sys.argv[1])
    num_of_wolves = int(sys.argv[2])
    num_of_moves = int(sys.argv[3])
    sheep_neighbourhood = int(sys.argv[4])
    wolf_neighbourhood = int(sys.argv[5])
except IndexError:
    num_of_sheeps = 200
    num_of_wolves = 5
    num_of_moves = 1000
    sheep_neighbourhood = 20
    wolf_neighbourhood = 30
    print("Inputs not all provided. " +
          "Defaulting to 200 sheep, 5 wolves, 1,000 moves, " + 
          "20 sheep neighbourhood and 30 wolf neighbourhood.")
except ValueError:
    num_of_sheeps = 200
    num_of_wolves = 5
    num_of_moves = 1000
    sheep_neighbourhood = 20
    wolf_neighbourhood = 30
    print("Inputs not valid integers. " +
          "Defaulting to 200 sheep, 5 wolves, 1,000 moves, " + 
          "20 sheep neighbourhood and 30 wolf neighbourhood.")

# Set whether message should be printed when a sheep is eaten based on input
silent_input = str(input("Receive message when a sheep is eaten? (Y/N):\n"))

# Set silent based on input. If not recognised, default to silent = True
if silent_input.upper() == "Y":
    print("Messages will not be muted.\n")
    silent = False
elif silent_input.upper() == "N":
    print("Messages will be muted.\n")
    silent = True
else:
    print("Could not recognise input. Messages will be muted.\n")
    silent = True
    
# Create empty lists for sheep and wolves
sheeps = []
wolves = []

# Draw plot
fig = matplotlib.pyplot.figure(figsize = (7,7), frameon = False)
#fig.add_axes([0, 0, 1, 1])

# Create sheeps
for i in range(num_of_sheeps):
    
    # Use data from web for xs and ys if it exists - after that use random int
    if i < len(td_ys):
        y = int(td_ys[i].text)
    else:
        y = None
    
    if i < len(td_xs):
        x = int(td_xs[i].text)
    else:
        x = None
    
    sheeps.append(agentframework.Sheep(id = i,
                                       x = x,
                                       y = y,
                                       environment = environment, 
                                       agents = sheeps,
                                       speed = 1))

# Create wolves
for i in range(num_of_wolves):
    wolves.append(agentframework.Wolf(id = i, 
                                      environment = environment, 
                                      agents = sheeps,
                                      speed = 3))

# Create stopping condition for animation - runs if true
carry_on = True

# Define update function for animation
def update(frame_number):
      
    global carry_on
    fig.clear()
    
    # Move sheeps
    for i in range(len(sheeps)):
        #print(sheeps[i])
        random.shuffle(sheeps)
        
        sheeps[i].eat()
        sheeps[i].throw_up()
        sheeps[i].move()
        sheeps[i].share_with_neighbours(sheep_neighbourhood)
    
    # Move wolves
    for i in range(len(wolves)):
        #print(wolves[i])
        random.shuffle(wolves)
        
        wolves[i].eat(wolf_neighbourhood, silent)
        wolves[i].move()
        

    # Plot environment
    matplotlib.pyplot.imshow(environment)
    matplotlib.pyplot.tick_params(left = False, right = False , 
                                  labelleft = False, labelbottom = False, 
                                  bottom = False)
    
    # Plot sheeps
    for i in range(len(sheeps)):
        matplotlib.pyplot.scatter(x = sheeps[i].x, y = sheeps[i].y,
                                  color = "white"
                                  )
    
    # Plot wolves
    for i in range(len(wolves)):
        matplotlib.pyplot.scatter(x = wolves[i].x, y = wolves[i].y,
                                  color = "black"
                                  )
        matplotlib.pyplot.xlim(0, len(environment[0]))
        matplotlib.pyplot.ylim(0, len(environment))
    
    
    # Create list of all sheeps stores
    # stores = [int(sheep.store) for sheep in sheeps]
    # print(stores)
    
    # Update stopping condition if all the sheep have been eaten
    if (len(sheeps) == 0):
        carry_on = False
        print("The wolves have won! All the sheep have been eaten!")
    
        with open("out.txt", "w", newline = "") as f2:
            writer = csv.writer(f2, delimiter = ",")
            for row in environment:
                writer.writerow(row)
                
        # Get list of sheeps current stores
        sheep_stores = []
        for sheep in sheeps:
            sheep_stores.append(sheep.store)
                    
        # Write sheeps current stores to a file
        with open("sheep stores.txt", "w", newline = "") as f3:
            writer = csv.writer(f3, delimiter = ",")
            writer.writerow(sheep_stores)

# Stop animation before max number of moves or if stopping condition met
def gen_function():
    global carry_on
    i = 0
    while (i < num_of_moves) & (carry_on):
        yield i
        i += 1
    else:
        carry_on = False
        print("Sheep left: " + str(len(sheeps)) + "\n" +
              "Survival rate: " + str(len(sheeps)/num_of_sheeps))
        
        # Write new environment
        with open("out.txt", "w", newline = "") as f2:
            writer = csv.writer(f2, delimiter = ",")
            for row in environment:
                writer.writerow(row)
                
        # Get list of sheeps current stores
        sheep_stores = []
        for sheep in sheeps:
            sheep_stores.append(sheep.store)
            
        # print(sheep_stores)
        
        # Write sheeps current stores to a file
        with open("sheep stores.txt", "a", newline = "") as f3:
            writer = csv.writer(f3, delimiter = ",")
            writer.writerow(sheep_stores)
            

# Save animation as GIF
animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, 
                                               repeat = False,
                                               frames = gen_function(),
                                               save_count = 100)

print("Saving animation...\n")

animation.save("sheep_and_wolves.gif", 
               writer = matplotlib.animation.PillowWriter(fps = 4))
               
print("Animation saved.")


"""
# Define function to pass to tkinter to run animation
def run():
    global animation
    animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, 
                                                   repeat = False, 
                                                   frames = gen_function())
    canvas.draw()

# Define function to pause the animation in tkinter    
def pause():
    try:
        animation.event_source.stop()
    except:
        print("No animation")
        

def exit_model():
    global root
    root.quit()
    root.destroy()

root = tkinter.Tk()
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, 
                                                             master = root)
canvas._tkcanvas.pack(side = tkinter.TOP, fill = tkinter.BOTH, expand = 1)
menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label = "Model", menu=model_menu)

# Add command to run model
model_menu.add_command(label= "Run model", command = run)

# Add command to pause model
model_menu.add_command(label = "Pause", command = pause)

# Add command to quit tkinter
model_menu.add_command(label = "Quit", command = exit_model)


tkinter.mainloop()

"""
