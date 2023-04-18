#-----Senior Design DNA Game-----#

import cv2
import os
import shutil
import mediapipe as mp
import tensorflow as tf
import pygame
import numpy

# import model functions from one dir above current dir
import sys
sys.path.append("..") 
import model_communication


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# open camera
cap = cv2.VideoCapture(0)

font_face = cv2.FONT_HERSHEY_SIMPLEX

# loading in model
model = tf.keras.models.load_model("../model_SIBI.h5")

#instructions for the user on how to play the game
instructions = ("Sign the Complementary Base")

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

# input however many sequences here
words = ["ATGCAT", "TATATAT", "TAGCTAC"]

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

stop = False
preparing_game = True

# Actual game begins, user starts signing 
frame_count = 0
word_idx = 0
letter_idx = 0

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
font = pygame.font.SysFont('courier', 40)
fontint = pygame.font.SysFont('courier', 28)
fontint.set_bold(True)

# general pygame process: render, then blit (need location), then display

box = pygame.image.load("box.png").convert_alpha()
#box.set_colorkey((255,255,255))
box = pygame.transform.scale(box, (60,60))
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (x,y))

# starting game
while stop == False:

    # prepare game UI showing the given DNA sequence, and blank boxes for what the user must sign/input
    if preparing_game:
        # fill resets the screen
        screen.blit(bg, (0,0))
        num_letters = len(words[word_idx])

        given_sequence = [font.render(letter, True, black) for letter in words[word_idx]]
        # blank sequence will be blank because letter color and background color are the same (blue, blue)
        blank_sequence = [font.render(letter, True, black) for letter in words[word_idx]]

        # finding locations for the letters
        given_loc = numpy.array([(int((x / (num_letters + 1)) * (i + 1)), int((x / 4))) for i in range(num_letters)])
        blank_loc = numpy.array([(int((x / (num_letters + 1)) * (i + 1)), int((3 * x / 4))) for i in range(num_letters)])

        # blitting and displaying
        for i in range(num_letters):
            screen.blit(given_sequence[i], given_loc[i])
            screen.blit(box, given_loc[i] - [18.5,9])
            #screen.blit(blank_sequence[i], blank_loc[i])
            screen.blit(box, blank_loc[i] - [18.5,9])
        screen.blit(fontint.render(instructions, True, black), (80, 60))
        pygame.display.update()
 
        # done setting up game display
        preparing_game = False

    ret, img = cap.read()
    imgFlipped = cv2.flip(img, 1)

    cv2.imwrite(f'{path}/frame.jpg', img)

    

    # every 5th frame is sent to model for prediction
    if frame_count % 5 == 0:
        classified_letter = model_communication.model(f"{path}/frame.jpg", model)

        # if correct, update pygame display
        if classified_letter == DNA_complement[words[word_idx][letter_idx]]:
            screen.blit(font.render(classified_letter, True, blue), blank_loc[letter_idx])
            pygame.display.update()

            # advance to next letter and check for finishing 
            # advances to next word if it exists, closes program if it does not
            if (letter_idx := letter_idx + 1) >= len(words[word_idx]):
                if (word_idx := word_idx + 1) >= len(words):
                    # maybe here instead of just breaking out of while loop and freeing resources
                    # can have like an ending pygame screen like "Thanks for playing!
                    # and then free resources
                    break
                else:
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
    cv2.putText(imgFlipped, str(classified_letter), (5, 100), font_face, 4, (255, 0, 0), 4, cv2.LINE_AA)

    cv2.imshow("Webcam Input", imgFlipped)

    frame_count += 1

    #checking events for stopping program
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
            stop = True
    if cv2.waitKey(100) == 27 or cv2.getWindowProperty("Webcam Input", cv2.WND_PROP_VISIBLE) < 1:
        stop = True

# free all resources used
pygame.quit()
cv2.destroyAllWindows()
cap.release()
shutil.rmtree(path)
