import cv2
from decode import decode
import numpy as np

NMSTHRESHOLD = 0.5
CONFTHRESHOLD = 0.8
'''
    Modification of main function from OpenCV tutorial https://github.com/opencv/opencv/blob/master/samples/dnn/text_detection.py
'''

def east_text_detector(image, confThreshold = CONFTHRESHOLD,  nmsThreshold = NMSTHRESHOLD, model = 'frozen_east_text_detection.pb'):

    (origH, origW) = image.shape[:2]
    (inpWidth, inpHeight) = (int(32 * np.floor(origW / 32)), int(32 * np.floor(origH / 32)))

    # Load network
    net = cv2.dnn.readNet(model)

    # Create a new named window
    outNames = []
    outNames.append("feature_fusion/Conv_7/Sigmoid")
    outNames.append("feature_fusion/concat_3")

    # Create a 4D blob from frame.
    blob = cv2.dnn.blobFromImage(image, 1.0, (inpWidth, inpHeight), (123.68, 116.78, 103.94), True, False)

    # Run the model
    net.setInput(blob)
    outs = net.forward(outNames)
    t, _ = net.getPerfProfile()

    # Get scores and geometry
    scores = outs[0]
    geometry = outs[1]
    [boxes, confidences] = decode(scores, geometry, confThreshold)

    # Apply NMS
    indices = cv2.dnn.NMSBoxesRotated(boxes, confidences, confThreshold, nmsThreshold)

    return boxes, indices


