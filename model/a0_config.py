import numpy as np
from os.path import join as pjoin
SEED = 42
TEST_SIZE = 0.2
VALID_SIZE = 0.1 # it is 10% of the training set

np.random.seed(SEED)
ABS_DIR = "/home/ec2-user/data/extracted"
aws_split_configuration = {
    "image_folder" : pjoin(ABS_DIR,"screenshot"),
    "bbox_folder" : pjoin(ABS_DIR,"bounding_box"),
    "layout_folder" : pjoin(ABS_DIR,"layouts"),
    "chart_folder" : pjoin(ABS_DIR,"chart"),
    "mark_folder" : pjoin(ABS_DIR,"marks"),
    "orientation_folder" : pjoin(ABS_DIR,"orientations")
}