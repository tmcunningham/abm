# Programming for Social Science Assessment 1: Agent Based Modelling practical

## Contents

This repository contains code to run an agent based model that simulates sheep and wolves in a field. This code was produced following the practical exercises for the GEO5995 module run by the University of Leeds.

Within the **python:** folder, this repository contains the following:
- **final_model.py:** file to be run to run the model
- **agentframework.py:** file containing the agent class and sheep and wolf subclasses used in the model
- **in.txt:**: text file containing the raster data for the sheeps' environment
- **other folders:** one folder per chapter of the module, containing earlier versions of the model and agent framework.

## Running the model

To run the model from the command line, the user should run the following from the directory where the model and agent framework scripts are saved:

	python final_model.py [num_of_sheeps] [num_of_wolves] [num_of_moves] [sheep_neighbourhood] [wolf_neighbourhood]

Where the arguments are:
- **[num_of_sheeps] (default: 200):** initial number of sheep in the model
- **[num_of_wolves]:** initial number of wolves in the model
- **[num_of_moves]:** number of iterations the model will run for, assuming some sheep survive this long
- **[sheep_neighbourhood]:** the distance sheep will look for another sheep to share their store with
- **[wolf_neighbourhood]:** distance wolves will be able to see (and eat) sheep from.
