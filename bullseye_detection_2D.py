import cv2
import numpy as np
from scipy.spatial import KDTree
# Import required modules
import cv2
import numpy as np
import pytesseract
from py360convert import e2c, c2e
from east_text_detector import east_text_detector
# from find_midpoint import find_midpoint
from find_midpoint_v2 import find_midpoint
from sklearn.cluster import KMeans
# Global constants
H_BOX_SCALING = 2
V_BOX_SCALING = 1.5
H_BOX_DIM = 200
V_BOX_DIM = 200
AREA_THREADHOLD = 400
SCALING_H_IMG = 1920
SCALING_V_IMG = 1080
COLOR_THEADHOLD = 140
BLUE_ = 0
RED_ = 2


def bullseye_text_detection_and_regcognition(orig_img, mode='legacy'):

    '''
    :param orig_img: Original pano image
    :param mode: legacy or modern mode
    :return: processed image and midpoint (x,y)
    '''

    image = e2c(orig_img, face_w = int(orig_img.shape[0]*2/3), mode='bilinear', cube_format='dice')
    temp_img = np.zeros(image.shape)
    orig = image.copy()
    (origH, origW) = image.shape[:2]
    (inpWidth, inpHeight) = (int(32 * np.floor(origW / 32)), int(32 * np.floor(origH / 32)))
    rW = origW / float(inpWidth)
    rH = origH / float(inpHeight)
    boxes, indices = east_text_detector(image)
    midP = []
    text_l = []
    count = 0

    # Loop through each box
    for i in indices:
        vertices = cv2.boxPoints(boxes[i[0]])
        # scale the bounding box coordinates based on the respective ratios
        vertices[:, 0] *= rW
        vertices[:, 1] *= rH
        o_h = int(boxes[i[0]][1][0])
        o_w = int(boxes[i[0]][1][0])
        width = int(boxes[i[0]][1][0] * H_BOX_SCALING)
        height = int(boxes[i[0]][1][1] * V_BOX_SCALING)
        area = o_h * o_w
        config = ("-l eng  --oem 1 --psm  13,7")


        # Choosing only horizontal rectangle and filter out boxes that have area less than 500
        if (width >= height  and  area >= AREA_THREADHOLD):
            src_pts = vertices.astype(np.float32)[0:3]
            dst_pts = np.array([[0, height - 1],
                                [0, 0],
                                [width - 1, 0],
                               ], dtype=np.float32)

            M = cv2.getAffineTransform(src_pts, dst_pts)

            # Directly warp the rotated rectangle to get the straightened rectangle
            crop_img = cv2.warpAffine(orig, M, (width, height))

            # Use tesseract to i
            text = pytesseract.image_to_string(crop_img, config=config)

            # Choosing argument based on mode: Legacy or modern
            if (mode == 'legacy'):
                arg =  ('-' in text) and (np.mean(crop_img[:,:,RED_]) > COLOR_THEADHOLD)
            else:
                arg =  ('-' in text) and (np.mean(crop_img[:, :, BLUE_]) > COLOR_THEADHOLD)

            if (arg):
                midX = (np.min(vertices[:, 0])) + (o_w / 2)
                midY = (np.min(vertices[:, 1])) + (o_h / 2)
                midP.append((midX, midY))
                text_l.append(text)
                print(text)
        count = count + 1

    if (not midP):
        midP.append((0, 0))
        text_l.append('No Bulleye Detected')

    p_array = np.asanyarray(midP)

    # Creating box for later reading
    s_x = H_BOX_DIM
    s_y = V_BOX_DIM
    new_text = []
    output = orig.copy()

    # Call find_midpoint to find the x and y coordinate of the mid point and a rectangular box cropped from the original image.
    cropped_img, mid_P_x, mid_P_y = find_midpoint(midP, p_array, text_l, rW, rH, origH, origW, s_x, s_y, output)

    # Read text from cropped image
    if (midP[0][0] != 0):
        '''
            Performing Text Recognition on the segmenting part
        '''
        print("Text from cropped image:")
        print("===================")
        config = ("-l eng --oem 1 --psm 6")
        text_l_n = (pytesseract.image_to_string(cropped_img[count], config=config)).splitlines()
        print(text_l_n)

        if(len(text_l) == 3):
            new_text.append(text_l_n)
        else:
            new_text = text_l
        # new_text.append(text_l_n)

        if(mid_P_y < 0 or mid_P_x < 0):
            mid_P_x = mid_P_y = 0
        temp_img[int(mid_P_y), int(mid_P_x)] = [0, 0, 255]
        count = count + 1
    else:
        new_text = ["No bullseye detected"]
        mid_P_x = mid_P_y = 0


    # Transform cube faces image to equirectangular

    c_to_e = c2e(temp_img, orig_img.shape[0], int(8 * np.floor(orig_img.shape[1] / 8)), cube_format='dice')
    index = np.where(c_to_e > 0)

    # Extract none zero midpoint
    if (np.isnan(np.mean(index[0])) or np.isnan(np.mean(index[1]))):
        m_x = 0
        m_y = 0
    else:
        m_x = np.mean(index[1])
        m_y = np.mean(index[0])

    img = orig_img
    if (m_x != 0):
        startX = int(max(0, m_x - s_x))
        endX = int(min(image.shape[1], m_x + s_x))
        startY = int(max(0, m_y - s_y))
        endY = int(min(image.shape[0], m_y + s_y))
        startX = int(startX)
        startY = int(startY)
        endX = int(endX)
        endY = int(endY)
        img = cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
    else:
        img = orig_img
    count = 1

    # Put text
    if(m_x != 0):

        for j in new_text:
            cv2.putText(img, j, (startX, startY - 150 + 50 * count), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 6, cv2.LINE_AA)
            count = count + 1
    else:
        cv2.putText(img, new_text[0], (int(img.shape[1]/2), int(img.shape[0]/2)), cv2.FONT_HERSHEY_TRIPLEX, 2, (0, 0, 255), 6, cv2.LINE_AA)

    t_img = cv2.resize(img, ((SCALING_H_IMG, SCALING_V_IMG)))

    return t_img, int(m_x) , int(m_y)