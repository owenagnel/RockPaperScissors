'''GestureAnalyst class analyses frames and returns drawn hand
and predicted gesture if one is found'''
import handtracker as ht
import torch
import model as cm
# pylint: disable=E1101

class GestureAnalyst():
    '''Analyses frames for gestures'''
    def __init__(self, weights_location = 'source/model/model_weights.pth'):
        self.model_weights_loc = weights_location
        self.handtracker = ht.HandDetector(max_num_hands=1,min_detection_confidence=0.5,
                                           min_tracking_confidence=0.5)
        self.classifier = cm.get_classifier()
        self.classifier.load_state_dict(torch.load('source/model/model_weights.pth'))
        self.classifier.eval()

    def analyse(self, frame):
        '''returns drawn frames and gesture (as an int from 0 to 2)'''
        gesture = None
        image, positions = self.handtracker.find_position(frame)
        if positions.any():
            tensor_rep = torch.from_numpy(positions)
            gesture = torch.argmax(self.classifier(tensor_rep)).item()
        return image, gesture
