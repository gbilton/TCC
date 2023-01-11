# Intelligent Traffic Light System with Sensors and Reinforcement Learning

This project presents an intelligent traffic light system that uses electromagnetic sensors to measure vehicle flow at intersections. The goal is to reduce traffic using reinforcement learning techniques trained on a neural network, to optimize the timing of the traffic light phase changes and minimize vehicle waiting time.

## Research Paper

The paper presents the development and implementation of the intelligent traffic light system discussed in this project. It includes detailed explanations of the methods used, simulation results, and analysis of the proposed solution.

The paper can be found in the Artigo.pdf file.

## Installation
The project requires Python 3 and the following libraries:

- Numpy
- Pandas
- Pytorch 
- (and others)


You can install all the required dependencies by running:
pip install -r requirements.txt


## Simulation

A simulator was built in Python to test and compare the performance of three distinct traffic control methods. The simulator includes maps, vehicles, and traffic lights. The base images were taken from Google Maps and the traffic constants such as maximum speed, accelerations, decelerations, and vehicle size were calibrated for a realistic representation. Each vehicle follows a pre-defined path and has sensors to detect other vehicles or traffic lights ahead, simulating human behavior.

## Results

The model was compared to three distinct traffic control methods, and showed promising results during the training phase. In the validation phase, the neural network was able to surpass traditional methods in some scenarios.




