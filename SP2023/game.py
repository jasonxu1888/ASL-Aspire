#-----Senior Design DNA Game-----#

import cv2
import os
import shutil
import mediapipe as mp
import tensorflow as tf
import pygame
import numpy
import random
import time

# import model functions from one dir above current dir
import sys
sys.path.append("..") 
import model_communication


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# open camera
cap = cv2.VideoCapture(0)

font_face = cv2.FONT_HERSHEY_DUPLEX

# loading in model
model = tf.keras.models.load_model("../model_SIBI.h5")

# starting and ending text
instructions = "Sign the Complementary Base!"
thanks = ("Thanks for Playing!")

# hard encode for the prediction
classes = {
    0:  'A',
    1:  'B',
    2:  'C',
    3:  'D',
    4:  'E',
    5:  'F',
    6:  'G',
    7:  'H',
    8:  'I',
    9:  'K',
    10: 'L',
    11: 'M',
    12: 'N',
    13: 'O',
    14: 'P',
    15: 'Q',
    16: 'R',
    17: 'S',
    18: 'T',
    19: 'U',
    20: 'V',
    21: 'W',
    22: 'X',
    23: 'Y'
}

DNA_complement = {
    "A": "T",
    "T": "A",
    "G": "C",
    "C": "G",
}

hands = mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
        )



# create empty folder for storing frames
# (probalby unecessary since never processing frames in the past...)
path = "frames"
if os.path.isdir(path):
    shutil.rmtree(path)
os.mkdir(path)

# set up pygame window
pygame.init()
x = 600
y = 600
screen = pygame.display.set_mode([x, y])

# simple UI elements
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0,0,0)
font = pygame.font.SysFont('courier', 28)
font.set_bold(True)

# mapping letters to UI elements
box = pygame.transform.scale(pygame.image.load("images/box.png").convert_alpha(), (60,60))
bg = pygame.transform.scale(pygame.image.load("images/bg.png"), (x,y))
box_letters = {
    "A" : pygame.transform.scale(pygame.image.load("images/box-A.png").convert_alpha(), (60,60)),
    "C" : pygame.transform.scale(pygame.image.load("images/box-C.png").convert_alpha(), (60,60)),
    "G" : pygame.transform.scale(pygame.image.load("images/box-G.png").convert_alpha(), (60,60)),
    "T" : pygame.transform.scale(pygame.image.load("images/box-T.png").convert_alpha(), (60,60))
}
base_structures = {
    "A" : pygame.transform.scale(pygame.image.load("images/base-A.png").convert_alpha(), (120,130)),
    "C" : pygame.transform.scale(pygame.image.load("images/base-C.png").convert_alpha(), (120,150)),
    "G" : pygame.transform.scale(pygame.image.load("images/base-G.png").convert_alpha(), (135,120)),
    "T" : pygame.transform.scale(pygame.image.load("images/base-T.png").convert_alpha(), (125,120))
}


# general pygame process: render, then blit (need location), then display
running = True
preparing_game = False
start_screen = True
frame_count = 0

# -1: not chosen yet by user
# 0: normal difficulty (letters)
# 1: advanced difficulty (base pictures)
difficulty = -1

# starting game
while running == True:

    # setup starting screen UI for displaying game information and choosing difficulty
    if start_screen:
        screen.blit(bg, (0,0))
        screen.blit(pygame.image.load("images/title-screen-resized.png").convert_alpha(), (59, 20))
        font.underline = True
        screen.blit(font.render(f"Instructions", True, black), (190, 110))
        screen.blit(font.render(f"Difficulties", True, black), (190, 230))
        font.underline = False
        screen.blit(font.render(instructions, True, black), (60, 150))
        screen.blit(font.render("Press 'n' for normal", True, black), (130, 270))
        screen.blit(font.render("Press 'a' for advanced", True, black), (110, 310))
        screen.blit(font.render("Made by ASL Aspire", True, black), (150, 400))
        screen.blit(pygame.transform.scale(pygame.image.load("images/logo-resized.png").convert_alpha(), (184,143)), (200, 440))
        pygame.display.update()
        start_screen = False

    #checking events for choosing difficulty and stopping program
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n: # normal
                preparing_game = True
                difficulty = 0
            if event.key == pygame.K_a: # advanced
                preparing_game = True
                difficulty = 1
        if event.type == pygame.QUIT:   
            running = False

    # prepare game UI showing the given DNA sequence, and blank boxes for what the user must sign/input
    if preparing_game:

        # resetting screen by blitting background
        screen.blit(bg, (0,0))

        # finding location of UI elements based on difficulty (if using boxed letters or chemical structures)
        if difficulty == 0:
            dictionary = box_letters

            length = random.randint(4, 8)
            word = "".join(random.choice("ACTG") for _ in range(length))
            letter_idx = 0

            given_loc = numpy.array([(int((x / (length + 1)) * (i + 1)) - 30, int((x / 4))) for i in range(length)])
            blank_loc = numpy.array([(int((x / (length + 1)) * (i + 1)) - 30, int((2.5 * x / 4))) for i in range(length)])
        if difficulty == 1:
            dictionary = base_structures

            length = 4
            word = "".join(random.choice("ACTG") for _ in range(4))
            letter_idx = 0

            given_loc = numpy.array([(int((x / (length)) * (i + 1)) - 55-80, int((x / 4))) for i in range(length)])
            blank_loc = numpy.array([(int((x / (length)) * (i + 1)) - 30-80, int((2.5 * x / 4))) for i in range(length)])


        # blitting UI elements
        for i in range(length):
            screen.blit(dictionary[word[i]], given_loc[i])
            screen.blit(box, blank_loc[i])

        # blitting instructions
        screen.blit(font.render(instructions, True, black), (60, 60))

        # rendering changes
        pygame.display.update()
 
        # done setting up game display
        preparing_game = False

    # do not proceed until difficulty is chosen
    if difficulty == -1:
        continue

    ret, img = cap.read()
    imgFlipped = cv2.flip(img, 1)

    cv2.imwrite(f'{path}/frame.jpg', img)

    # every 5th frame is sent to model for prediction
    if frame_count % 25 == 0:
        classified_letter = model_communication.model(f"{path}/frame.jpg", model)

        # if correct, update pygame display
        if classified_letter == DNA_complement[word[letter_idx]]:
            screen.blit(box_letters[classified_letter], blank_loc[letter_idx])
            pygame.display.update()

            # advance to next letter and check for finished word
            if (letter_idx := letter_idx + 1) >= len(word):
                letter_idx = 0
                preparing_game = True
    
    # adding back mediapipe annotations
    # mediapipe suggestion for improving performance
    imgFlipped.flags.writeable = False
    imgFlipped = cv2.cvtColor(imgFlipped, cv2.COLOR_BGR2RGB) # convert to RGB for processing
    results = hands.process(imgFlipped)
    imgFlipped.flags.writeable = True
    imgFlipped = cv2.cvtColor(imgFlipped, cv2.COLOR_RGB2BGR) # convert back to BGR to display proper colors
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
            imgFlipped,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    
    # writing the prediction on the camera
    cv2.putText(imgFlipped, str(classified_letter), (5, 100), font_face, 4, black, 4, cv2.LINE_AA)

    cv2.imshow("Webcam Input", imgFlipped)

    frame_count += 1

    # stop program if webcam window closed
    if cv2.waitKey(100) and cv2.getWindowProperty("Webcam Input", cv2.WND_PROP_VISIBLE) < 1:
        running = False

# free cam resource (so face is not 'paused' in video)
cv2.destroyAllWindows()
cap.release()

# ending "thank you" screen
screen.blit(bg, (0,0))
screen.blit(pygame.image.load("images/logo-resized.png").convert_alpha(), (116, 90))
screen.blit(font.render(thanks, True, black), (135, 400))
pygame.display.update()
time.sleep(2)

# free resources
pygame.quit()
shutil.rmtree(path)
