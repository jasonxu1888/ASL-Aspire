import cv2
import time
import os
import shutil
import random
import mediapipe as mp
import tensorflow as tf
import model_communication

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

"""
SUPER IMP: 
HERE IS ANOTHER SOLUTION THAT WOULD OVERLAY MediaPipe's ANNOTATION ONTO IMAGE
https://www.geeksforgeeks.org/face-and-hand-landmarks-detection-using-python-mediapipe-opencv/ 
"""



# define list of words to spell out
words = ['K', 'ATOM']
currentWordIndex = 0
currentLetterIndex = 0
killSwitch = False

# SET THE COUNTDOWN TIMER
# for simplicity we set it to 3
# We can also take this as input
TIMER = int(3)
font = cv2.FONT_HERSHEY_SIMPLEX
# Open the camera
cap = cv2.VideoCapture(0)

#loading in the ML model
model = tf.keras.models.load_model('/Users/daniel/Documents/Senior_Design_Project/model_SIBI.h5')

# Hard Encode for the Prediction
classes = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
    4: 'E',
    5: 'F',
    6: 'G',
    7: 'H',
    8: 'I',
    9: 'K',
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

with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    STOP = False

    count = 0

    if os.path.exists('Webcam_Pictures/'):
        # if the user already has a file path called Webcam_Pictures, we want to
        # create a unique new file path that they do not have
        path = "Webcam_Pictures_uniquename" + str(random.random()) + str(random.random())
    else:
        path = "Webcam_Pictures"
    while STOP == False:

        # Read and display each frame
        ret, img = cap.read()

        imgFlipped = cv2.flip(img, 1)

        ##putting mediapipe onto hands before start
        ##MEDIAPIPE'S SUGGESTION ON IMP PERFORMANCE:
        imgFlipped.flags.writeable = False
        imgFlipped = cv2.cvtColor(imgFlipped, cv2.COLOR_BGR2RGB)
        results = hands.process(imgFlipped)

        # MEDIAPIPE'S DRAWING ANNOTATIONS ON IMAGE:
        imgFlipped.flags.writeable = True
        imgFlipped = cv2.cvtColor(imgFlipped, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    imgFlipped,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        position = ((int)(img.shape[1] / 2) - 520, (int)(img.shape[0] / 2))
        position_shifted_down = ((int)(img.shape[1] / 2 - 250), (int)(img.shape[0] / 2 + 100))
        cv2.putText(imgFlipped, "Press Space to Begin!", position, font, 3, (218, 112, 214), 4, cv2.LINE_AA)
        cv2.putText(imgFlipped, "At Any Time Press Esc To Quit", position_shifted_down, font, 1, (218, 112, 214), 4,
                    cv2.LINE_AA)
        cv2.imshow('Webcam Input', imgFlipped)

        # check for the key pressed
        keyInput = cv2.waitKey(125)

        # set the key for the countdown
        # to begin. Here we set q
        # if key pressed is q
        if keyInput == ord(' '):
            prev = time.time()

            while ((TIMER > 0) & (STOP == False)):
                if keyInput == 27:
                    ##this will stop the countdown, terminating the program
                    STOP = True

                ret, img = cap.read()

                # Display countdown on each frame
                # specify the font and draw the
                # countdown using puttext
                imgFlipped = cv2.flip(img, 1)

                ##putting mediapipe onto the countdown hands:
                ##MEDIAPIPE'S SUGGESTION ON IMP PERFORMANCE:
                imgFlipped.flags.writeable = False
                imgFlipped = cv2.cvtColor(imgFlipped, cv2.COLOR_BGR2RGB)
                results = hands.process(imgFlipped)

                # MEDIAPIPE'S DRAWING ANNOTATIONS ON IMAGE:
                imgFlipped.flags.writeable = True
                imgFlipped = cv2.cvtColor(imgFlipped, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            imgFlipped,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())

                # "position" is actually being used as a font color
                cv2.putText(imgFlipped, str(TIMER),
                            (520, 260), font,
                            7, position,
                            4, cv2.LINE_AA)
                cv2.imshow('Webcam Input', imgFlipped)
                keyInput = cv2.waitKey(125)

                # current time
                cur = time.time()

                # Update and keep track of Countdown
                # if time elapsed is one second
                # than decrease the counter
                if cur - prev >= 1:
                    prev = cur
                    TIMER = TIMER - 1

            cv2.destroyWindow('Webcam Input')
            # makes a directory to store all pictures
            os.mkdir(path)
            os.chdir(path)

            ##this is the actual part where user will do signs
            while cap.isOpened() & STOP == False:

                if keyInput == 27:
                    STOP = True

                ret, img = cap.read()
                imgFlipped = cv2.flip(img, 1)

                cv2.imwrite('frame{:d}.jpg'.format(count), img)

                ##MEDIAPIPE'S SUGGESTION ON IMP PERFORMANCE:
                imgFlipped.flags.writeable = False
                imgFlipped = cv2.cvtColor(imgFlipped, cv2.COLOR_BGR2RGB)
                results = hands.process(imgFlipped)

                # MEDIAPIPE'S DRAWING ANNOTATIONS ON IMAGE:
                imgFlipped.flags.writeable = True
                imgFlipped = cv2.cvtColor(imgFlipped, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            imgFlipped,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())



                # every 5 pictures are being sent to classification
                if count % 150 == 0:
                    ##SENDING IT TO THE MODEL TO PREDICT
                    classified_letter = model_communication.model(
                        "/Users/daniel/Documents/Senior_Design_Project/" + path + "/frame{:d}.jpg".format(count), model)

                cv2.putText(imgFlipped, str(int(count / 30)),
                            (10, 10), font,
                            0.5, position,
                            2, cv2.LINE_AA)
                ##if they have not reached the end of the words, display the letter they are currently on
                if killSwitch == False:
                    cv2.putText(imgFlipped, words[currentWordIndex],
                            (100, 50), font,
                            2, position,
                            2, cv2.LINE_AA)
                    cv2.putText(imgFlipped, words[currentWordIndex][currentLetterIndex],
                                ((int)(img.shape[1] / 2 + 500), 50), font,
                                2, (218, 112, 214),
                                2, cv2.LINE_AA)
                else:
                    ## if they have reached the end, give them nice farewell message
                    position = ((int)(img.shape[1] / 2) - 520, (int)(img.shape[0] / 2))
                    position_shifted_down = ((int)(img.shape[1] / 2 - 165), (int)(img.shape[0] / 2 + 100))
                    cv2.putText(imgFlipped, "Thank You For Playing!", position, font, 3, (218, 112, 214), 4, cv2.LINE_AA)
                    cv2.putText(imgFlipped, "Press Esc To Quit", position_shifted_down, font, 1,
                                (218, 112, 214), 4,
                                cv2.LINE_AA)

                ##writing the prediction on the camera
                cv2.putText(imgFlipped, str(classified_letter),
                            (0, 700), font,
                            4, position,
                            4, cv2.LINE_AA)

                cv2.imshow("Snapshot", imgFlipped)

                ##NOW update your letter in the word if the user got the letter right

                if killSwitch != True and str(classified_letter) == words[currentWordIndex][currentLetterIndex]:
                    print("here")
                    if currentLetterIndex < (len(words[currentWordIndex]) - 1):
                        print("updating letter index" + str(currentLetterIndex))
                        currentLetterIndex += 1
                    else:
                        currentWordIndex += 1
                        currentLetterIndex = 0
                        print("new word" + str(currentWordIndex) + "new letter index" + str(currentLetterIndex))
                        if currentWordIndex >= len(words):
                            killSwitch = True



                count += 30  # i.e. at 30 fps, this advances one second
                cap.set(1, count)
                # removing the picture every second
                if (count >= 870):
                    os.remove('frame{:d}.jpg'.format(count - 870))

                # Display the clicked frame for 2
                # sec.You can increase time in
                # waitKey also
                # cv2.imshow('Snapshot', img)

                # time for which image displayed
                keyInput = cv2.waitKey(125)

                # HERE we can reset the Countdown timer
                # if we want more Capture without closing
                # the camera

        # Press Esc to exit
        elif keyInput == 27:
            break

# close the camera
cap.release()

os.chdir('../')

shutil.rmtree(path)
# close all the opened windows
cv2.destroyAllWindows()

##DIFFERENT SOLUTION


# Create an object to hold reference to camera video capturing
# vidcap = cv2.VideoCapture(0)

# #check if connection with camera is successfully
# while vidcap.isOpened():
#     ret, frame = vidcap.read()  #capture a frame from live video

#     #check whether frame is successfully captured
#     if ret:
#         # continue to display window until 'q' is pressed
#         morePictures = True
#         while(morePictures):
#             cv2.imshow("Frame",frame)   #show captured frame

#             #press 'q' to break out of the loop
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#             # if '):
#             #     morePictures = False
#     #print error if frame capturing was unsuccessful
#     else:
#         print("Error : Failed to capture frame")

# # print error if the connection with camera is unsuccessful
# else:
#     print("Cannot open camera")