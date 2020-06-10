# *Method to Perform 3D Localization of Text in Shipboard Point Cloud Data Using Corresponding 2D Image*
Created by Adrian Mai, Dr Mark Bilinski, Raymond Provost - NIWC Pacific <br />
![full prediction](https://github.com/quocanh010/MP3LTSPC/blob/master/display_images/full.png)

## Introduction
This work is based on our ...link..., which is going to appear in IEEE ICCE 2020. <br />
3D object detection and localization have been major focuses for the computer vision community for the past several years. However, extracting informa-tion from a 3D point cloud is often a more cumbersome and labor intensive task compared to just 2D images. 2D techniques are more mature and also have far more labelled training data. The contribution of this work is to leverage 2D computer vision techniques on a panorama image and use that to extract information from the 3D point cloud, in the case where there is an existing cor-respondence between the panorama and the point cloud. Performance of the algorithm will be based on 2D object detection, and 3D position and rotation of the object. The objects of interest are text placards called "bullseyes" that are found throughout US Navy ships. 3D data of this type of environment is limited, impacting the ability of researchers to develop and test their algorithms. Another contribution of this work is making available a large corpus of shipboard LiDAR scan data from the museum ship USS Midway. <br />
Index Terms-Object Localization, Point Cloud, Computer Vision, Machine Learning. <br />
## Data
Another contribution of this work is making available
a large corpus of shipboard LiDAR scan data from the
museum ship USS Midway.  <br />
The whole dataset for this project contains in  https://drive.google.com/open?id=1-JmWPIzUmuzz9g-f-XLtgj808bcN0QhE <br />
### Software requirement: <br />
FARO SCENCE LT: https://knowledge.faro.com/Software/FARO_SCENE/SCENE/Software_Download_Installation_and_Release_Notes_for_SCENE_LT <br />
The input to our algorithm is .xyz and pano images.  This software can convert the scanner data into those formats.  An example workflow is provided below. <br />
### Test data (already extracted from Faro Scene lt Midway data) <br />
Test data is on "Midway_contain_bulleyes_pics" with panorama images and "Midway_contain_xyz" <br />
### Full midway data: <br />
Please download the rest of the data present from a google drive
## Faro Scene lt Data Extraction tutorial 
This is a tutorial on how to extract data from a faro pointcloud project <br />
### 1. Import project: 
- To import project open FARO SCENE software then click Import then direct to the location of the complete faro project. Double click on the project <br />
![import  project1](https://github.com/quocanh010/MP3LTSPC/blob/master/display_images/1.jpg)
### 2. Export xyz scan data:
- To export xyz data. Right click on the whole scan -> Export -> Scans -> Scans-Ordered  <br />
![export  scans1](https://github.com/quocanh010/MP3LTSPC/blob/master/display_images/3.jpg)  <br />
- Next very important step is to make sure to check on the "Export each scan into a separate file." This will allow Faro to export each individual scan.  <br />
- Choose an appropriate folder then click Export at the bottom  <br />
![export  scans2](https://github.com/quocanh010/MP3LTSPC/blob/master/display_images/4.jpg)
### 3. Export panorama image data:
- To export pano image data. Right click on the whole scan -> Export -> Panoramic Images -> Scans Resolution. Then pick an appropriate folder <br />
![export  pano](https://github.com/quocanh010/MP3LTSPC/blob/master/display_images/5.jpg)
## Installation
Requires: Python 3
To install all the required python packages fro the project: 
```bash
pip install requirements.txt 
```

## Usage
After downloading the test data to appropriate folders run the command in terminal:
```bash
python main.py --mode legacy --image_folder Midway_contain_bulleyes_pics --xyz_folder Midway_contain_xyz --result_folder result_image
```

## License
Our code is released under MIT License (see LICENSE file for details).

## Selected Projects that Use Our Project
TBD
## Citation
....
