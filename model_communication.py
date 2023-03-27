# Hard Encode for the Prediction
import pandas as pd
import numpy as np
import tensorflow as tf
import time
from tensorflow.keras import layers
import mediapipe as mp
import os
import csv
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tensorflow.keras.utils import to_categorical
# from google.colab import drive
# from google.colab.patches import cv2_imshow
import tensorflow.keras
import extract_features
import tensorflow


def model(webcam_input_path, ml_model) :
    starttime = time.time()
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
        9 : 'J',
        10: 'K',
        11: 'L',
        12: 'M',
        13: 'N',
        14:'O',
        15:'P',
        16:'Q',
        17:'R',
        18:'S',
        19:'T',
        20:'U',
        21:'V',
        22:'W',
        23:'X',
        24:'Y',
        25 : 'Z'
    }

    # Directly from Imageset Dataset Testing
    #Load Image and do Feature Extraction
    #path_to_image = "/content/drive/MyDrive/Webcam_Project/Coding/ColabResources/archive/SIBI_datasets_LEMLITBANG_SIBI_R_90.10_V02/SIBI_datasets_LEMLITBANG_SIBI_R_90.10_V02/test/C (2).jpg"
    test_image = webcam_input_path
    (wristX, wristY, wristZ,
     thumb_CmcX, thumb_CmcY, thumb_CmcZ,
     thumb_McpX, thumb_McpY, thumb_McpZ,
     thumb_IpX, thumb_IpY, thumb_IpZ,
     thumb_TipX, thumb_TipY, thumb_TipZ,
     index_McpX, index_McpY, index_McpZ,
     index_PipX, index_PipY, index_PipZ,
     index_DipX, index_DipY, index_DipZ,
     index_TipX, index_TipY, index_TipZ,
     middle_McpX, middle_McpY, middle_McpZ,
     middle_PipX, middle_PipY, middle_PipZ,
     middle_DipX, middle_DipY, middle_DipZ,
     middle_TipX, middle_TipY, middle_TipZ,
     ring_McpX, ring_McpY, ring_McpZ,
     ring_PipX, ring_PipY, ring_PipZ,
     ring_DipX, ring_DipY, ring_DipZ,
     ring_TipX, ring_TipY, ring_TipZ,
     pinky_McpX, pinky_McpY, pinky_McpZ,
     pinky_PipX, pinky_PipY, pinky_PipZ,
     pinky_DipX, pinky_DipY, pinky_DipZ,
     pinky_TipX, pinky_TipY, pinky_TipZ,
     output_IMG) = extract_features.extract_feature(test_image)



    #print(wristX, wristY,
    #      thumb_CmcX, thumb_CmcY, thumb_McpX, thumb_McpY, thumb_IpX, thumb_IpY, thumb_TipX, thumb_TipY,
    #      index_McpX, index_McpY, index_PipX, index_PipY, index_DipX, index_DipY, index_TipX, index_TipY,
    #      middle_McpX, middle_McpY, middle_PipX, middle_PipY, middle_DipX, middle_DipY, middle_TipX, middle_TipY,
    #      ring_McpX, ring_McpY, ring_PipX, ring_PipY, ring_DipX, ring_DipY, ring_TipX, ring_TipY,
    #      pinky_McpX, pinky_McpY, pinky_PipX, pinky_PipY, pinky_DipX, pinky_DipY, pinky_TipX, pinky_TipY)
    # plt.axis("on")
    # plt.imshow(cv.cvtColor(output_IMG, cv.COLOR_BGR2RGB))
    # plt.show()


    #Shape the image features into an 1x3 array.
    input_IMG = np.array([[[wristX], [wristY], [wristZ],
                         [thumb_CmcX], [thumb_CmcY], [thumb_CmcZ],
                         [thumb_McpX], [thumb_McpY], [thumb_McpZ],
                         [thumb_IpX], [thumb_IpY], [thumb_IpZ],
                         [thumb_TipX], [thumb_TipY], [thumb_TipZ],
                         [index_McpX], [index_McpY], [index_McpZ],
                         [index_PipX], [index_PipY], [index_PipZ],
                         [index_DipX], [index_DipY], [index_DipZ],
                         [index_TipX], [index_TipY], [index_TipZ],
                         [middle_McpX], [middle_McpY], [middle_McpZ],
                         [middle_PipX], [middle_PipY], [middle_PipZ],
                         [middle_DipX], [middle_DipY], [middle_DipZ],
                         [middle_TipX], [middle_TipY], [middle_TipZ],
                         [ring_McpX], [ring_McpY], [ring_McpZ],
                         [ring_PipX], [ring_PipY], [ring_PipZ],
                         [ring_DipX], [ring_DipY], [ring_DipZ],
                         [ring_TipX], [ring_TipY], [ring_TipZ],
                         [pinky_McpX], [pinky_McpY], [pinky_McpZ],
                         [pinky_PipX], [pinky_PipY], [pinky_PipZ],
                         [pinky_DipX], [pinky_DipY], [pinky_DipZ],
                         [pinky_TipX], [pinky_TipY], [pinky_TipZ]]])

    #print(input_IMG.shape)
    #print(input_IMG)

    # model = tf.keras.models.load_model('/Users/daniel/Documents/Senior_Design_Project/model_SIBI.h5')


    #Print the Prediction
    predict_x = ml_model.predict(input_IMG)
    print("\nPrediction is done")
    ###print(model.predict_classes(input_IMG))
    classes_x=np.argmax(predict_x,axis=1)
    print("The sign you are imaging is:")
    print(classes[classes_x[0]])
    endtime = time.time()
    print("\nTime it took to classify: ")
    print(endtime - starttime, " sec")
    return classes[classes_x[0]]
