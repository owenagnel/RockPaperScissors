'''Test module to check that gesture is correctly recognized'''
import statistics
import random
import cv2
import gestureanalyst
import artist



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

        # reset scores
        computer_score = 0
        player_score = 0

        while True:
            # rock paper scissor start sequence
            cv2.waitKey(200)
            start_seq = artist.get_start_seq()
            for i, image in enumerate(start_seq):
                cv2.imshow('Rock Paper Scissor', image)
                if i % 2 == 0:
                    cv2.waitKey(100)
                else:
                    cv2.waitKey(700)

            # Record 6 frames and pass to model to determine gesture
            i = 0
            gestures = []
            while i <= 5:
                _, frame = cap.read()
                # Detections
                image, gesture = analyst.analyse(frame)
                if gesture is not None:
                    i += 1
                    gestures.append(gesture)
                image = artist.get_main(image, computer_score, player_score, None, gesture)
                cv2.imshow('Rock Paper Scissor', image)
                cv2.waitKey(1)
            #gesture is the most common gesture recorded !BUG mode could return several vals
            player_gesture = statistics.mode(gestures)
            computer_gesture = random.randint(0,2) #computer move

            # Looks up result in table
            result = win_lookup[player_gesture][computer_gesture]
            if result == -1:
                computer_score += 1
            elif result == 1:
                player_score +=1

            # output webcam feed with updated main screen
            for _ in range(50):
                _, frame = cap.read()
                frame, _ = analyst.analyse(frame)
                image = artist.get_main(frame, computer_score, player_score,
                                        computer_gesture, player_gesture)
                cv2.imshow('Rock Paper Scissor', image)
                cv2.waitKey(5)
            # comp vs player sequence
            for image in artist.result(computer_gesture,player_gesture):
                cv2.imshow('Rock Paper Scissor', image)
                cv2.waitKey(1000)

            # show player the result of the throw
            if result == -1:
                cv2.imshow('Rock Paper Scissor', artist.lose_pt())
                cv2.waitKey(700)
            elif result == 1:
                cv2.imshow('Rock Paper Scissor', artist.win_pt())
                cv2.waitKey(700)
            else:
                cv2.imshow('Rock Paper Scissor', artist.draw())
                cv2.waitKey(700)

            # check scores are not too big
            if player_score == 3:
                cv2.imshow('Rock Paper Scissor', artist.player_win())
                cv2.waitKey(1000)
                break
            if computer_score == 3:
                cv2.imshow('Rock Paper Scissor', artist.comp_win())
                cv2.waitKey(1000)
                break

            #show blank before starting loop again
            cv2.imshow('Rock Paper Scissor', artist.blank)

        # Once game has ended, display play again sceen,
        # allow player to play again or quit
        cv2.imshow('Rock Paper Scissor', artist.play_again)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main_loop()
