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

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# define list of words to spell out
words = ["K", "ATOM"]

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

while stop == False:

    # Read and display each frame
    ret, img = cap.read()

    imgFlipped = cv2.flip(img, 1)

    position = ((int)(img.shape[1] / 2) - 520, (int)(img.shape[0] / 2))
    position_shifted_down = ((int)(img.shape[1] / 2 - 250), (int)(img.shape[0] / 2 + 100))
    cv2.putText(imgFlipped, "Space to Begin/Esc To Quit", position_shifted_down, font, 1, (218, 112, 214), 4, cv2.LINE_AA)
    cv2.imshow("Webcam Input", imgFlipped)

    
    # 'space' to start game
    # 'esc' to exit game
    keyInput = cv2.waitKey(125)
    if keyInput == ord(' '):
        break
    elif keyInput == 27:
        stop = True
        
# Actual game begins, user starts signing 
frame_count = 0
word_idx = 0
letter_idx = 0

while stop == False:

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