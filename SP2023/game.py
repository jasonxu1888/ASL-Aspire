#-----Simplified version of Senior_Design_WordGames.py-----#

import cv2
import os
import shutil
import mediapipe as mp
import tensorflow as tf

# import from one dir above current dir
import sys
sys.path.append("..") 

import model_communication
import pygame

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# define list of words to spell out
pygame.init()
x = 600;
y = 600;
screen = pygame.display.set_mode([x, y])

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

words = ["ATGC"]
wordscomp = [''];
for letter in words[0]:
            if letter == "A":
                wordscomp[0] += "T"
            elif letter == "G":
                wordscomp[0] += "C"
            elif letter == "T":
                wordscomp[0] += "A"
            elif letter == "C":
                wordscomp[0] += "G"
bases = len(words[0]);
font = pygame.font.Font('freesansbold.ttf', 32)
text_list = [];
text_list2 = [];
textRect = [];
textRect2 = [];
for i in range(bases):
    text_list.append(font.render(words[0][i], True, green, blue))
for i in range(bases):
    text_list2.append(font.render(wordscomp[0][i], True, green, blue))


for i in range(bases):
    textRect.append(text_list[i].get_rect())
for i in range(bases):
    textRect2.append(text_list2[i].get_rect())

for i in range(bases):
    textRect[i].center = (int(x/(bases+1))*(i+1), int(x/4))
for i in range(bases):
    textRect2[i].center = (int(x/(bases+1))*(i+1), int(3 * x / 4))
# Open the camera
cap = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX

#loading in the ML model
model = tf.keras.models.load_model("../model_SIBI.h5")

# Hard Encode for the Prediction
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

hands = mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
        )



# create empty folder for storing frames
# probalby unecessary since never processing past frames...
path = "frames"
if os.path.isdir(path):
    shutil.rmtree(path)
os.mkdir(path)

stop = False
        
# Actual game begins, user starts signing 
frame_count = 0
word_idx = 0
letter_idx = 0
screen.fill(white);
while stop == False:
    for i in range(bases):
        screen.blit(text_list[i], textRect[i])
    for i in range(bases):
        screen.blit(text_list2[i], textRect2[i])
    for event in pygame.event.get():

        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
            # deactivates the pygame library
            pygame.quit()

            # quit the program.
            quit()

        # Draws the surface object to the screen.
        pygame.display.flip()

    ret, img = cap.read()
    imgFlipped = cv2.flip(img, 1)

    cv2.imwrite(f'{path}/frame.jpg', img)

    # mediapipe suggestion for improving performance
    imgFlipped.flags.writeable = False

    # every 5th frame is sent to model for prediction
    # check if user sign is correct, and update work/letter indexes
    if frame_count % 5 == 0:
        classified_letter = model_communication.model(f"{path}/frame.jpg", model)
        if classified_letter == words[word_idx][letter_idx]:
            if (letter_idx := letter_idx + 1) >= len(words[word_idx]):
                if (word_idx := word_idx + 1) >= len(words):
                    break
                else:
                    letter_idx = 0
    
    # writing the prediction on the camera
    cv2.putText(imgFlipped, str(classified_letter), (5, 100), font, 4, (255, 0, 0), 4, cv2.LINE_AA)
    
    # @TODO can consider adding back the mediapipe annotations before displaying frame

    cv2.imshow("Webcam Input", imgFlipped)

    frame_count += 1

    keyInput = cv2.waitKey(125)
    if keyInput == 27:
        stop = True

# free all resources used
cap.release()
shutil.rmtree(path)
cv2.destroyAllWindows()