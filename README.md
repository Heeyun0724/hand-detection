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
If you want to download each package from vscode cmd
```python
pip install tqdm == 4.66.1
pip install mediapipe == 0.10.9
pip install opencv-python == 4.9.0.80
pip install json
pip install numpy == 1.26.3
```

If you want to download packages from the vscode cmd window to requirements_hand.txt at once
```python
pip install -r requirements_hand.txt
```

## :memo: Files
`video hand detection Angle.py` Extract the angle

`video hand detection coordinate.py` Extract x,y,z three-dimensional coordinates

## Usage 
If you want finger angle extraction, run video hand detection Angle.py in vscode.

If you want finger coordinate extraction, run video hand detection coordinate.py in vscode.

## Result
The information on the finger extracted in the path specified by you is saved as a json file.

The json file is printed separately with both hands, and five fingers are generated as individual json files. The result will be a total of 10 json files.

If the hand was not detected in the video, it was made to be printed in an empty array in the json file.
