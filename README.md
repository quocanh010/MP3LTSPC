## *Method to Perform 3D Localization of Text in Shipboard Point Cloud Data Using Corresponding 2D Image*
Created by Adrina Mai, Dr Mark Bilinski, Raymond Provost - NIWC Pacific

![prediction example](https://github.com/charlesq34/pointnet/blob/master/doc/teaser.png)

### Introduction
This work is based on our ...link..., which is going to appear in IEEE ICCE 2020. 3D object detection and localization have been major focuses for the computer vision community for the past several years. However, extracting informa-tion from a 3D point cloud is often a more cumbersome and labor intensive task compared to just 2D images. 2D techniques are more mature and also have far more labelled training data. The contribution of this work is to leverage 2D computer vision techniques on a panorama image and use that to extract information from the 3D point cloud, in the case where there is an existing cor-respondence between the panorama and the point cloud. Performance of the algorithm will be based on 2D object detection, and 3D position and rotation of the object. The objects of interest are text placards called "bullseyes" that are found throughout US Navy ships. 3D data of this type of environment is limited, impacting the ability of researchers to develop and test their algorithms. Another contribution of this work is making available a large corpus of shipboard LiDAR scan data from the museum ship USS Midway. Index Terms-Object Localization, Point Cloud, Computer Vision, Machine Learning.

### Citation
....
   
### Installation
Requires: Python 3
To install all the required python packages fro the project:
```bash
pip install requirements.txt 
```
### DATA
Software requirement:
FARO SCENCE LT: https://knowledge.faro.com/Software/FARO_SCENE/SCENE/Software_Download_Installation_and_Release_Notes_for_SCENE_LT
The software to extract .xyz and pano images 
The whole data set of the Midway Museum is inlcuded in the following google drive https://drive.google.com/open?id=1-JmWPIzUmuzz9g-f-XLtgj808bcN0QhE
Test data:
Test data is on "Midway_contain_bulleyes_pics" with panorama images and "Midway_contain_xyz"


Full midway data:


### Usage
After downloading the test data to appropriate folders run the command in terminal:
```bash
python main.py --mode legacy --image_folder Midway_contain_bulleyes_pics --xyz_folder Midway_contain_xyz --result_folder result_image
```

### License
Our code is released under MIT License (see LICENSE file for details).

### Selected Projects that Use Our Project
TBD
