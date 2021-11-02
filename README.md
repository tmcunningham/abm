# Programming for Social Science Assessment 1: Sheep and Wolves Agent Based Model

This repository contains code to run an agent based model that simulates sheep eating grass in a field, while wolves hunt the sheep. This code was produced following the practical exercises for the GEOG5995 module run by the University of Leeds.

## Contents

Within the **python** folder, this repository contains the following:
- **final_model.py:** file to be run to run the model
- **agentframework.py:** file containing the agent class and sheep and wolf subclasses used in the model
- **in.txt:** text file containing the raster data for the sheeps' environment
- **other folders:** one folder per chapter of the module (except chapter 3), containing earlier versions of the model and agent framework.

## The model

### Running the model

To run the model from the command line, the user should run the following in the directory where the model, agent framework and input files are saved:

	python final_model.py [num_of_sheeps] [num_of_wolves] [num_of_moves] [sheep_neighbourhood] [wolf_neighbourhood]

Where the arguments are (default values given after argument names):
- ```[num_of_sheeps] = 200```: initial number of sheep in the model
- ```[num_of_wolves] = 5```: initial number of wolves in the model
- ```[num_of_moves] = 1000```: number of iterations the model will run for, assuming some sheep survive this long
- ```[sheep_neighbourhood] = 20```: the distance sheep will look for another sheep to share their store with
- ```[wolf_neighbourhood] = 30```: distance wolves will be able to see (and eat) sheep from.

Please note, **all** of the arguments must be specified. If arguments are missing, or if they are not provided as integers, the default values will be used in the model.

When the above code is run, a GUI will be launched with a "Model" dropdown icon in the menu bar. The "Model" dropdown has three options:
- **Run model:** initiate the model. An animation will begin to play in the current window.
- **Pause:** when the model is running, pause the animation. Select "Run model" again to resume.
- **Quit:** end instance of tkinter.

Once the model has been started, it cannot be re-run without restarting the programme.

### How the model works

The model simulates 

