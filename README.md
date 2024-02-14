# :hand:HAND DETECTION
# Extraction of finger x,y,z coordinate & Angle by finger 

#### Project execution period : 2024.01 ~ 2024.02

-----------------------
## Description
Insert the video with the input data and extract the angle and x,y,z three-dimensional coordinates for the hand recognized as a media pipe.

### 1. function list
|Sortation|Function|realization|
|------|---|---|
|S/W|extract the angle|Python|
|S/W|extract x,y,z three-dimensional coordinates|Python|

## Environment

> Vscode
> 
> Python Version 3.10 (Window)

## Prerequisite
> Python
> 
> import cv2
> 
> import mediapipe as mp
> 
>import numpy as np
> 
> import json
> 
> from tqdm import tqdm

## Version
```python
pip install tqdm == 4.66.1
pip install mediapipe == 0.10.9
pip install opencv-python == 4.9.0.80
pip install json
pip install numpy == 1.26.3
```

## :memo: Files
`video hand detection Angle.py` Extract the angle

`video hand detection coordinate.py` Extract x,y,z three-dimensional coordinates

## Usage 
If you want finger angle extraction, run video hand detection Angle.py in vscode.

If you want finger coordinate extraction, run video hand detection coordinate.py in vscode.
