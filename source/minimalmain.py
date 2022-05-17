'''Test module to check that gesture is correctly recognized'''
import statistics
import random
import cv2
import gestureanalyst
import time
import os

lookup = ["Rock", "Paper", "Scissor"]
BOLD = '\033[1m'
DEFAULT = '\033[0m'
rock = [
        " _____            _",
        "|  __ \          | |",
        "| |__) |___   ___| | __",
        "|  _  // _ \ / __| |/ /",
        "| | \ \ (_) | (__|   <",
        '|_|  \_\___/ \___|_|\_\\']
paper = [
        " _____                ",
        "|  __ \                     ",
        "| |__) |_ _ _ __   ___ _ __ ",
        "|  ___/ _` | '_ \ / _ \ '__|",
        "| |  | (_| | |_) |  __/ |   ",
        "|_|   \__,_| .__/ \___|_|   ",
        "           | |              ",
        "           |_|              ",]

scissor = [
        "   _____      _     ",
        "  / ____|    (_)                   ",
        " | (___   ___ _ ___ ___  ___  _ __ ",
        "  \___ \ / __| / __/ __|/ _ \| '__|",
        "  ____) | (__| \__ \__ \ (_) | |   ",
        " |_____/ \___|_|___/___/\___/|_|"]
shoot = [
        "   _____ _                 _   ",
        "  / ____| |               | |  ",
        " | (___ | |__   ___   ___ | |_ ",
        "  \___ \| '_ \ / _ \ / _ \| __|",
        "  ____) | | | | (_) | (_) | |_ ",
        " |_____/|_| |_|\___/ \___/ \__|"
        ]

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

def main_loop():
    '''Overlays the name of the gestur on top of video output'''
    cap = cv2.VideoCapture(0)
    win_lookup = [[0,-1,1],[1,0,-1],[-1,1,0]]
    analyst = gestureanalyst.GestureAnalyst()
    computer_score = 0
    player_score = 0

    while cap.isOpened():
        os.system('clear')
        time.sleep(1)
        print("Ready? Press 's' to start and 'q' to quit.")
        choice = input()
        if choice == 'q':
            break

        i = 0
        while i <= 2000:
            _, frame = cap.read()
            # Detections
            image, gesture = analyst.analyse(frame)
            if gesture is not None:
                i += 1
                image = addtext(lookup[gesture], image)
            cv2.imshow('Rock Paper Scissor', image)
            cv2.waitKey(10)
        # reset scores
        computer_score = 0
        player_score = 0

        while True:
            # rock paper scissor start sequence
            os.system('clear')
            time.sleep(1)
            for s in rock:
                print(s)
            time.sleep(1)
            os.system('clear')
            for s in paper:
                print(s)
            time.sleep(1)
            os.system('clear')
            for s in scissor:
                print(s)
            time.sleep(1)
            os.system('clear')
            for s in shoot:
                print(s)
            # Record 6 frames and pass to model to determine gesture
            i = 0
            gestures = []
            while i <= 20:
                _, frame = cap.read()
                # Detections
                image, gesture = analyst.analyse(frame)
                if gesture is not None:
                    i += 1
                    gestures.append(gesture)
                    image = addtext(lookup[gesture], image)
                cv2.imshow('Rock Paper Scissor', image)
                cv2.waitKey(10)
            #gesture is the most common gesture recorded
            player_gesture = statistics.mode(gestures)
            computer_gesture = random.randint(0,2) #computer move
            os.system('clear')
            print("Player chose: " + lookup[player_gesture])
            print("Computer chose: " + lookup[computer_gesture])

            # Looks up result in table
            result = win_lookup[player_gesture][computer_gesture]
            if result == -1:
                computer_score += 1
            elif result == 1:
                player_score +=1

            print("")
            # show player the result of the throw
            if result == -1:
                print("Computer wins a point")
            elif result == 1:
                print("Player wins a point")
            else:
                print("Draw")

            time.sleep(4)
            os.system('clear')

            print(f"Player: {player_score}")
            print(f"Computer: {computer_score}")
            time.sleep(2)
            # check scores are not too big
            if player_score == 3:
                print("Player wins!")
                time.sleep(2)
                break
            if computer_score == 3:
                print("Computer wins...")
                time.sleep(2)
                break

        # Once game has ended, display play again sceen,
        # allow player to play again or quit
        print("Do you want to play again? (y/n)")
        if input() == 'n':
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main_loop()
