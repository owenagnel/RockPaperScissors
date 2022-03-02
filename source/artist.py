'''Class to draw game graphics onto screen'''
import cv2
import cvzone

rock = cv2.imread("graphics/RockPaperScissorSeq/Rock.png", cv2.IMREAD_UNCHANGED)
scissor = cv2.imread("graphics/RockPaperScissorSeq/Scissor.png", cv2.IMREAD_UNCHANGED)
paper = cv2.imread("graphics/RockPaperScissorSeq/Paper.png", cv2.IMREAD_UNCHANGED)
blank = cv2.imread("graphics/RockPaperScissorSeq/Blank.png", cv2.IMREAD_UNCHANGED)
shoot = cv2.imread("graphics/RockPaperScissorSeq/Shoot.png", cv2.IMREAD_UNCHANGED)
play_again = cv2.imread("graphics/PlayAgain.png", cv2.IMREAD_UNCHANGED)

def get_start_seq():
    return [blank, rock, blank, paper, blank, scissor, blank, shoot]

def get_ready():
    return cv2.imread("graphics/Ready.png", cv2.IMREAD_UNCHANGED)

locations = {
    "c1" : "graphics/scores/Comp1.png",
    "c2" : "graphics/scores/Comp2.png",
    "c3" : "graphics/scores/Comp3.png",
    "p1" : "graphics/scores/Player1.png",
    "p2" : "graphics/scores/Player2.png",
    "p3" : "graphics/scores/player3.png",
    "cr" : "graphics/Choices/CompRock.png",
    "cp" : "graphics/Choices/CompPaper.png",
    "cs" : "graphics/Choices/CompScissor.png",
    "pr" : "graphics/Choices/PlayerRock.png",
    "pp" : "graphics/Choices/PlayerPaper.png",
    "ps" : "graphics/Choices/PlayerScissor.png"
}

player_choices = {
    0 : "pr",
    1 : "pp",
    2 : "ps"
}
player_scores = {
    1 : "p1",
    2 : "p2",
    3 : "p3"
}
comp_choices = {
    0 : "cr",
    1 : "cp",
    2 : "cs"
}
comp_scores = {
    1 : "c1",
    2 : "c2",
    3 : "c3"
}

def get_main(image, comp_score, player_score, comp_gesture, player_gesture):
    main = cv2.imread("graphics/Mainscreen.png", cv2.IMREAD_UNCHANGED)
    image = cvzone.overlayPNG(image,main, [0,0])
    if player_gesture is not None:
        gesture_overlay = cv2.imread(locations[player_choices[player_gesture]], cv2.IMREAD_UNCHANGED)
        image = cvzone.overlayPNG(image,gesture_overlay, [0,0])
    if comp_score:
        score_overlay = cv2.imread(locations[comp_scores[comp_score]], cv2.IMREAD_UNCHANGED)
        image = cvzone.overlayPNG(image,score_overlay, [0,0])
    if player_score:
        score_overlay = cv2.imread(locations[player_scores[player_score]], cv2.IMREAD_UNCHANGED)
        image = cvzone.overlayPNG(image,score_overlay, [0,0])
    if comp_gesture is not None:
        gesture_overlay= cv2.imread(locations[comp_choices[comp_gesture]], cv2.IMREAD_UNCHANGED)
        image = cvzone.overlayPNG(image,gesture_overlay, [0,0])
    return image

def lose_pt():
    return cv2.imread('graphics/CompPoint.png', cv2.IMREAD_UNCHANGED)

def win_pt():
    return cv2.imread('graphics/PlayerPoint.png', cv2.IMREAD_UNCHANGED)

def draw():
    return cv2.imread('graphics/Draw.png', cv2.IMREAD_UNCHANGED)

def comp_win():
    return cv2.imread('graphics/outcome/You_lose.png', cv2.IMREAD_UNCHANGED)

def player_win():
    return cv2.imread('graphics/outcome/You_win.png', cv2.IMREAD_UNCHANGED)