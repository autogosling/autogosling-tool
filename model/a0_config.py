import numpy as np
from os.path import join as pjoin
SEED = 42
TEST_SIZE = 0.2
VALID_SIZE = 0.1 # 10% of the training set

np.random.seed(SEED)
ABS_DIR = "/home/ec2-user/data/extracted"
aws_split_config = {
    "image_folder" : pjoin(ABS_DIR,"screenshot"),
    "bbox_folder" : pjoin(ABS_DIR,"bounding_box"),
    "layout_folder" : pjoin(ABS_DIR,"layouts"),
    "chart_folder" : pjoin(ABS_DIR,"chart"),
    # "mark_folder" : pjoin(ABS_DIR,"marks"),
    "orientation_folder" : pjoin(ABS_DIR,"orientations")
}

split_config = aws_split_config

CLASS_FOLDER_NAMES = ["chart","layout","orientation"]
CLASS_FOLDERS = [folder+"_folder" for folder in CLASS_FOLDER_NAMES]
BBOX_FOLDER = "bbox_folder"
IMAGE_FOLDER = "image_folder"
YOLOV7_LABELS = "labels" # this is the name of the folder that a3_generate_yolov7.py will generate
YOLOV7_IMAGES = "images" # this is the name of the folder that a3_generate_yolov7.py will generate