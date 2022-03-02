'''Module for generating rock paper scissor dataset'''
import math
import numpy as np
import pandas as pd
import cv2
import handtracker


class DataCollector:
    '''A class that automates data collection for hand gestures.
    Asks user to perform gestures, then stores data to csv file.
    Attributes
    __________
    fileloc : str
        Name and location of the output csv file
    gestures : List(str)
        List of the names of various gestures you wish to collect. Labels in csv doc
        will be ordered in the same way (i.e. first gesture will have label 0 etc...)
    device_index : int
        Device index for videocapture, 0 by default'''

    def __init__(self, fileloc='source/data/data.csv', gestures=None, device_index = 0):
        if gestures is None:
            gestures = ["Rock", "Paper", "Scissor"]
        self.dictionary = {v: k for v, k in enumerate(gestures)}
        self.gestures = len(self.dictionary)
        self.fileloc = fileloc
        self.device_index = device_index
        self.frame_shape = self.get_webcam_shape()
        print(self.frame_shape)

    def get_webcam_shape(self):
        '''Gets the shape of frames produced by webcam'''
        cap = cv2.VideoCapture(self.device_index)
        _ , frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        return frame.shape


    def addtext(self, text, image):
        '''Adds text overlay to image'''
        white = (255,255,255)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_size = 1.75
        font_color = white
        font_thickness = 2
        loc_x,loc_y = 50,670
        img_text = cv2.putText(image, text, (loc_x,loc_y), font,
                               font_size, font_color, font_thickness, cv2.LINE_AA)
        return img_text

    def black_text(self, text):
        '''Returns a black image with written text'''
        return self.addtext(text, np.zeros((self.frame_shape[0],
                                            self.frame_shape[1],3), dtype = "uint8"))

    def save(self, data_frame):
        '''Saves the input dataframe to the csv file'''
        assert data_frame.shape[1] == 64
        data_frame.to_csv(self.fileloc, header=False, mode='a', index=False)

    def add_to_df(self, landmarks, data_frame, label: int):
        '''writes the numpy array into a temporary dataframe df,
        written to csv at the end of loop iteration'''
        landmarks = np.append(landmarks, [label])
        temporary = pd.DataFrame(landmarks.reshape(1,-1), columns=list(data_frame))
        return data_frame.append(temporary, ignore_index=True)

    def collect(self):
        '''Data gathering'''
        iterations = int(input("How many iterations? ") or "3")
        runs = int(input("How many runs per iteration? ") or "50")
        hand_detector = handtracker.HandDetector(max_num_hands=1, min_detection_confidence=0.8,
                                                 min_tracking_confidence=0.8)

        cap = cv2.VideoCapture(self.device_index)
        flag = False
        for i in range(iterations*self.gestures):
            unsaved = True
            while unsaved:
                if cap.isOpened():
                    text = (self.dictionary[i%self.gestures]
                            + f": iteration {math.floor(i/self.gestures) + 1} of {iterations}"
                            + " begins soon...")
                    image = self.black_text(text)
                    cv2.imshow("Webcam feed", image)
                    cv2.waitKey(3000) #Let user prepare

                    data_frame = pd.DataFrame(columns = np.arange(64)) #initialise temp dataframe
                    j = 0 # number of frames collected
                    while j < runs:
                        _ , frame = cap.read() # Read from webcam
                        image, landmarks = hand_detector.find_position(frame)
                        image = (self.addtext(self.dictionary[i%self.gestures]
                                + f" {j+1} of {runs}", image)) #
                        cv2.imshow("Webcam feed", image)

                        if landmarks.any():
                            print(self.dictionary[i % self.gestures] + ": " +str(j))
                            data_frame = self.add_to_df(landmarks, data_frame, i% self.gestures)
                            j+=1

                        if cv2.waitKey(10) & 0xFF == ord('q'): #press q to exit
                            flag = True # Allows us to break past all loops
                            break
                    if flag:
                        break
                    image = self.black_text("Good? (y/n)")
                    cv2.imshow("Webcam feed", image)
                    if cv2.waitKey(0) & 0xFF != ord('n'):
                        self.save(data_frame)
                        unsaved = False
            if flag:
                break
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    collector = DataCollector()
    collector.collect()
