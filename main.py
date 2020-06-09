import argparse
import pandas as pd
import cv2
from bullseye_detection_2D import bullseye_text_detection_and_regcognition
from os import listdir
import numpy as np
import time
import pytesseract
start = time.time()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Get Arguments from user
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", type=str, default="legacy", help="bullseye type: legacy or modern")
ap.add_argument("-if", "--image_folder", type=str, default="Midway_contain_bulleyes_pics", help="path to pano input images")
ap.add_argument("-xf", "--xyz_folder", type=str, default="Midway_contain_xyz", help="path to .xyz folder")
ap.add_argument("-rf", "--result_folder", type=str, default="result_image", help="path to processed image folder")
args = vars(ap.parse_args())

# mode = args["mode"]
# xyz_folder_name = args['xyz_folder']
# pano_folder_name = args['image_folder']
# out_result = args['result_folder']

mode = "legacy"
xyz_folder_name = "Midway_contain_xyz"
pano_folder_name = "Midway_contain_bulleyes_pics"
out_result = "result_image"

name_l = sorted(listdir(xyz_folder_name))
name_p = sorted(listdir(pano_folder_name))
xyzCenter_list = []

def main():
    '''
        The main fuction will import the xyz file then create a grid mapping between the rgb image and the 3D xyz data.
        Then it will call the bullseye_text_detection_and_regcognition to obtain the mid point and the processed image with bounding box
        Lastly the function will save the processed image to a folder and also those midpoints into a numpy array.
    '''
    xyz_center_list = []
    mid_p_l = []
    count = 0

    for name in name_l:

        # Process 3D data
        data = pd.read_csv(xyz_folder_name + '/' + name, sep='\s+', header=None)

        '''
            data with 8 columns contains grid (u,v) = 0:2; xyz = 2:5; rgb = 5:8
            xyz_grid: is the grid mapping between 2D and 3D
        '''

        grid_data = data.iloc[:, 0:2].to_numpy()
        xyz_data = data.iloc[:, 2:5].to_numpy()
        xyz_grid = np.zeros((grid_data[:, 0].max() + 1, grid_data[:, 1].max() + 1, 3))
        xyz_grid[grid_data[:, 0], grid_data[:, 1]] = xyz_data

        # Read pano image
        image = cv2.imread(pano_folder_name + '/' + name_p[count])

        # Bullseye detection in 2D
        img, mid_x, mid_y = bullseye_text_detection_and_regcognition(image.astype(np.uint8),  mode)
        mid_p_l.append((name, [mid_x, mid_y]))
        print(mid_p_l[count])
        cv2.imwrite(out_result + '/' + name + '.png', img)

        # Get the location in 3D
        xyz_predicted = xyz_grid[mid_y, mid_x]
        xyz_center_list.append(xyz_predicted)
        count = count + 1

    # Save xyz data into xyz_center array
    np.save('xyz_center.npy', np.asarray(xyz_center_list))

if __name__ == '__main__':
    main()
#     Command line for testing
#     python main.py --mode legacy --image_folder Midway_contain_bulleyes_pics --xyz_folder Midway_contain_xyz --result_folder result_image