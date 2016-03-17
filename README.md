# destruction_scenarios_generator
This repository contains the scripts and assets required to create the destruction scenarios that are available in the destruction_scenarios repository. The scripts run in Blender (https://www.blender.org) and are designed to automatically create and destroy the scenarios.

## Installation
To run the scripts, two Blender addons must be installed/activated. The first one, Cell Fracture, comes with Blender and only needs to be activated. To do this, go to Blender preferences (Ctrl-Alt-U), select the Add-ons tab, search for "Cell Fracture" and tick the activation box on the right. The second one, Bullet Constraints Tool, must be downloaded and installed according to https://bwide.wordpress.com/scripts/bullet-constraints-tools. After the installation is complete, activate it with the same method as with Cell Fracture.

## Setup
To run the scripts, setting an environment variable pointing to the root of the package is required so that the script can locate the assets. The name of the variable is DESTRUCTION_SCENARIO_ROOT and it should point to the folder containing this file. If Blender is run on the shell where the variable is set, everything should work correctly.

## General Use Instructions
There are three scripts: common.py, house.py and garage.py. The former contains functions and methodologies that are shared by the other two and cannot be used on its own. Each of the other two produce a scenario: a House and a Garage, respectively. Both of these contain a boolean global variable named "SIMULATE", which defined whether the scenario is merely created or whether destruction is also applied. We recommend first trying the script with the variable set to False, and running the simulation takes a long time (several hours, depending on the computer where it is being run).

## Considerations
The scripts were tested and successfully used with Blender 2.76b and with Bullet Constraints Tool 0.3.7.4.

## License and Citing
The code and meshes present in this repository are subject to the GPL license, as described in LICENSE.md. The textures were downloaded from the internet and are royalty free.

If you wish to use the scenario generator in your work and publish it, please cite this work as such: "Destruction Scenario Dataset Generator", http://www.roboptics.pt
