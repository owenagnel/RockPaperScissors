# RockPaperScissors
A rock paper scissors game that uses machine learning to recognise the correct gesture

## Getting started
There are a number of python modules:
- handtracker.py: defineds the HandTracker class which does all of the hand tracking and information extraction using mediapipe.
- datacollector.py: Defines a datacollector class that takes a list of gestures and a file path. It then asks the user to perform each gesture a set amount of times and saves all the landmark points oouput by mediapipe to a csv file along with a label.
- gesturedataset.py: defines a dataset to be used to train the model in gesture recognition. Reads the csv file from a passed location
- model.py: defines a generic FNN classifier neural network and trains it on the above dataset. Very specific to this project, perhaps a better implementation in the futures.
- main.py: a demo of the model operating correctly; in the future the actual game logic needs to be added.
