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

# Open the camera
cap = cv2.VideoCapture(0)

font_face = cv2.FONT_HERSHEY_SIMPLEX

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

DNA_complement = {
    "A": "T",
    "T": "A",
    "G": "C",
    "C": "G",
}

words = ["ATGC", "TATATATAT"]

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
font = pygame.font.Font('freesansbold.ttf', 40)


# num_bases = len(words[0])
# text_list = []
# text_list2 = []
# textRect = []
# textRect2 = []
# for i in range(num_bases):
#     text_list.append(font.render(words[0][i], True, green, blue))
# for i in range(num_bases):
#     text_list2.append(font.render(wordscomp[0][i], True, green, blue))


# for i in range(num_bases):
#     textRect.append(text_list[i].get_rect())
# for i in range(num_bases):
#     textRect2.append(text_list2[i].get_rect())

# for i in range(num_bases):
#     textRect[i].center = (int(x/(num_bases+1))*(i+1), int(x/4))
# for i in range(num_bases):
#     textRect2[i].center = (int(x/(num_bases+1))*(i+1), int(3 * x / 4))

# render, then blit, then display

while stop == False:
    
    # prepare game interface showing the given DNA sequence, and blanks for what the user must sign/input
    if preparing_game:
        # fill resets the screen
        screen.fill(white)

        num_letters = len(words[word_idx])

        given_sequence = [font.render(letter, True, green, blue) for letter in words[word_idx]]
        # blank sequence will be blank because letter color and background color are the same (blue, blue)
        blank_sequence = [font.render(letter, True, blue, blue) for letter in words[word_idx]]

        # finding locations for the letters
        given_loc = [(int((x / (num_letters + 1)) * (i + 1)), int((x / 4))) for i in range(num_letters)]
        blank_loc = [(int((x / (num_letters + 1)) * (i + 1)), int((3 * x / 4))) for i in range(num_letters)]

        # blitting and displaying
        for i in range(num_letters):
            screen.blit(given_sequence[i], given_loc[i])
            screen.blit(blank_sequence[i], blank_loc[i])
        pygame.display.update()
 
        # done setting up game display
        preparing_game = False

    ret, img = cap.read()
    imgFlipped = cv2.flip(img, 1)

    cv2.imwrite(f'{path}/frame.jpg', img)

    # mediapipe suggestion for improving performance
    imgFlipped.flags.writeable = False

    # every 5th frame is sent to model for prediction
    # check if user signs correct DNA complement
    if frame_count % 5 == 0:
        classified_letter = model_communication.model(f"{path}/frame.jpg", model)

        # if correct, update pygame display
        if classified_letter == DNA_complement[words[word_idx][letter_idx]]:
            screen.blit(font.render(classified_letter, True, green, blue), blank_loc[letter_idx])
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
    
    # writing the prediction on the camera
    cv2.putText(imgFlipped, str(classified_letter), (5, 100), font_face, 4, (255, 0, 0), 4, cv2.LINE_AA)
    
    # @TODO can consider adding back the mediapipe annotations before displaying frame

    cv2.imshow("Webcam Input", imgFlipped)

    frame_count += 1

    #checking events for stopping program
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            stop = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            stop = True
    if cv2.waitKey(100) == 27 or cv2.getWindowProperty("Webcam Input", cv2.WND_PROP_VISIBLE) < 1:
        stop = True

# free all resources used
pygame.quit()
cv2.destroyAllWindows()
cap.release()
shutil.rmtree(path)
