# RockPaperScissors
A rock paper scissors game that uses machine learning to recognise the correct gesture

## Getting started
To get started, you simply need to run main.py.

If you're interested in recording your own data and retraining teh model, do the following:

Recording the data is done using the datacollector.py module. Run as main and specify number of iterations of gesture collection and number of frames collected for each iteration. It's possible your webcam has a different deviec index to the default one specified, if this is the case, when the `DataCollector()` object is initiated in the `__main__` if statement, pass `device_index = your device index`. All the collected landmarks with their correct label should be added to a csv document in teh data folder.

Next train the model by running model.py as main. It will initiate a dataset automatically using the gesturedataset.py module. If your data is in a different location, make sure to update the parameters for the dataset generator. Hyperparameters can be found at the top of the model.py module.

Once the model has been trained, its weights will be saved in the model/ folder. 

You can now run main.py and play rock paper scissors.

## Module explanaion
There are a number of python modules:
- handtracker.py: defineds the HandTracker class which does all of the hand tracking and information extraction using mediapipe.
- datacollector.py: Defines a datacollector class that takes a list of gestures and a file path. It then asks the user to perform each gesture a set amount of times and saves all the landmark points oouput by mediapipe to a csv file along with a label.
- gesturedataset.py: defines a dataset to be used to train the model in gesture recognition. Reads the csv file from a passed location
- model.py: defines a generic FNN classifier neural network and trains it on the above dataset. Very specific to this project, perhaps a better implementation in the futures.
- main.py: a demo of the model operating correctly; in the future the actual game logic needs to be added.
