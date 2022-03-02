'''Test module to check that gesture is correctly recognized'''
import cv2
import gestureanalyst
import artist
import statistics
import random
# pylint: disable=E1101



def main_loop():
    '''Overlays the name of the gestur on top of video output'''
    cap = cv2.VideoCapture(0)
    win_lookup = [[0,-1,1],[1,0,-1],[-1,1,0]]
    analyst = gestureanalyst.GestureAnalyst()
    computer_score = 0
    player_score = 0


    while cap.isOpened():
        ready = artist.get_ready()
        cv2.imshow('Rock Paper Scissor', ready)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
        game = True

        while game:
            cv2.waitKey(200)
            start_seq = artist.get_start_seq()
            for i, image in enumerate(start_seq):
                cv2.imshow('Rock Paper Scissor', image)
                if i % 2 == 0:
                    cv2.waitKey(100)
                else:
                    cv2.waitKey(700)

            _, frame = cap.read()
            i = 0
            gestures = []
            while i <= 20:
                _, frame = cap.read()
                # Detections
                image, gesture = analyst.analyse(frame)
                if gesture is not None:
                    i += 1
                    gestures.append(gesture)
                image = artist.get_main(image, computer_score, player_score, None, gesture)
                cv2.imshow('Rock Paper Scissor', image)
                cv2.waitKey(10)

            player_gesture = statistics.mode(gestures)
            computer_gesture = random.randint(0,2)
            print(player_gesture, computer_gesture)

            result = win_lookup[player_gesture][computer_gesture]
            if result == -1:
                computer_score += 1
            elif result == 1:
                player_score +=1

            print( player_score, computer_score)

            for _ in range(40):
                _, frame = cap.read()
                image = artist.get_main(frame, computer_score, player_score,
                                        computer_gesture, player_gesture)
                cv2.imshow('Rock Paper Scissor', image)
                cv2.waitKey(10)

            if result == -1:
                cv2.imshow('Rock Paper Scissor', artist.lose_pt())
                cv2.waitKey(700)
            elif result == 1:
                cv2.imshow('Rock Paper Scissor', artist.win_pt())
                cv2.waitKey(700)
            else:
                cv2.imshow('Rock Paper Scissor', artist.draw())
                cv2.waitKey(700)

            if player_score == 3:
                cv2.imshow('Rock Paper Scissor', artist.player_win())
                cv2.waitKey(700)
                break
            elif computer_score == 3:
                cv2.imshow('Rock Paper Scissor', artist.comp_win())
                cv2.waitKey(700)
                break
            cv2.imshow('Rock Paper Scissor', artist.blank)



        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main_loop()
