'''Module used for HAnd tracking. Uses a mediapipe to find 21 landmark points for hand.'''
import cv2
import mediapipe as mp
import numpy as np

class HandDetector():
    '''Initialises the hand tracker model from mediapipe'''
    def __init__(self, static_image_mode=False,
                 max_num_hands=2,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.mode = static_image_mode
        self.max_hands = max_num_hands
        self.min_detection_conf = min_detection_confidence
        self.min_track_conf = min_tracking_confidence

        #Initialise tracking model
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands, 1,
                                         self.min_detection_conf,
                                         self.min_track_conf)
        self.result = None

    def find_hands(self, frame, drawhands=True):
        '''Takes a BGR image finds landmarks, returns the image
        with or without drawn landmarks'''
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb = cv2.flip(image_rgb, 1)
        image_rgb.flags.writeable = False
        self.result = self.hands.process(image_rgb)
        image_rgb.flags.writeable = True
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        if self.result.multi_hand_landmarks:
            for hand in self.result.multi_hand_landmarks:
                if drawhands:
                    self.mp_drawing.draw_landmarks(image_bgr,
                            hand, self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing.DrawingSpec(color=(100, 100, 100),
                                                        thickness=2, circle_radius=4),
                            self.mp_drawing.DrawingSpec(color=(51, 50, 50),
                                                        thickness=2, circle_radius=2),
                            )
        return image_bgr

    def find_position(self, frame, hand_num = 0):
        '''Returns the xyz position of 21 landmark points of hand number hand_num in numpy array'''
        image = self.find_hands(frame, True) #runs the frame through the model to get result

        landmark_list = np.zeros(21*3)

        if self.result.multi_hand_landmarks:
            hand_lms = self.result.multi_hand_landmarks[hand_num]

            landmark_list = np.array([[result.x, result.y, result.z]
                                       for result in hand_lms.landmark]).flatten()

        return (image, np.float32(landmark_list))




def main():
    '''Demo of the module: Opens webcam feed and draws hand landmarks'''
    hand_detector = HandDetector()
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        _ , frame = cap.read()
        image = hand_detector.find_hands(frame)
        landmarks = hand_detector.find_position(frame)
        if landmarks:
            print(landmarks[8])
        cv2.imshow("Webcam feed", image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
