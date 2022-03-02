'''Test module to check that gesture is correctly recognized'''
import cv2
import handtracker as ht
import torch
import model as cm
# pylint: disable=E1101

dictionary = {0: "Rock", 1: "Paper", 2: "Scissor"}

def addtext(text, image):
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

def main():
    '''Overlays the name of the gestur on top of video output'''
    handtracker = ht.HandDetector(max_num_hands=1,min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    classifier = cm.get_classifier()
    classifier.load_state_dict(torch.load('source/model/model_weights.pth'))
    classifier.eval()

    while cap.isOpened():
        _, frame = cap.read()

        # Detections
        image, positions = handtracker.find_position(frame)
        if positions.any():
            tensor_rep = torch.from_numpy(positions)
            result = torch.argmax(classifier(tensor_rep)).item()
            assert result >= 0 & result <= 2
            image = addtext(dictionary[result], image)


        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
