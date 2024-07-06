# Smart CCTV
# Introduction
CCTV (Closed-circuit television) is a remote monitoring system using cameras (video surveillance).\
The broadcasts are usually transmitted to a limited (closed) number of monitors, unlike “regular” TV,\
which is broadcast to the public at large.\
CCTV networks are commonly used to detect and deter criminal activities, and record traffic infractions, but they have other uses,\
such as disaster management, medical monitoring and diagnosis, city and community street monitoring, behavioral research etc.

The idea of "Smart" CCTV can be implemented using Computer Vision techniques and algorithms,\
such as object detection and human behavior recognition (HAR).\
This could be done in real-time monitoring or in post-processing, using recorded data from cameras.

This project implements "Smart CCTV" system, with object detection and HAR using OpenCV.

# Project Structure and Description
```
└── 📁smart_cctv 
    └── smart_cctv.py                       => interesting frames filtering with object detection
    └── 📁human_activity_recognition
        └── Actions.txt                     => human activity classes
        └── HAR.py                          => running HAR
        └── resnet-34_kinetics.onnx         => Resnet34 pre-trained model
    └── live_detection.py                   => YOLOv3 object detection using live camera recording
    └── smart_cctv_core.py                  => main system functions, including YOLOv3
    └── 📁utils
        └── data_format_converter.py        => converting video stream to images and vice versa
        └── play_sequence.py                => video-streaming for frames sequence (i.e after object detection)
```
The "Smart CCTV" system functions as follows:
* On input data (images), creating foreground model using background subtraction algorithm, utilizing MOG,\
  (Mixture Of Gaussians).
* Performing noise filtering on frame with masked background, using morphological opening.
* Running connected components labeling (Spaghetti), filtering under defined threshold.
* Filtering only the interesting frames, i.e where the change/action in the scene happens,\
  also with minimal number of frames, required to track the scene change (according to scene),\
  thus, reducing insignificant details and processed data amount.

Then, the system performs object detection and HAR in real-time or in post-processing state.

For object detection, the model used is Tiny YOLOv3 (with reduced number of convolutional layers).\
![](https://github.com/DMTRBor/object_tracker/blob/master/utils/od.png)

For HAR, CNN Resnet34 architecture is used, trained on kinetic dataset, which includes 400 classes of activities.\
![](https://github.com/DMTRBor/object_tracker/blob/master/utils/har.png)

To run HAR, the following commands supported:
For video-stream processing:
```
cd human_activity_recognition
python HAR.py --model resnet-34_kinetics.onnx --classes Actions.txt --input videos/example_activities.mp4 --gpu 1 --output output.mp4
```
For live camera recording:
```
cd human_activity_recognition
python HAR.py --model resnet-34_kinetics.onnx --classes Actions.txt
```

# Installation
To clone the repository:
```
git clone https://github.com/DMTRBor/smart_cctv.git
```

Start with Python>=3.8 environment

To install virtual environment, use:
```
python -m venv .env
.env\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
