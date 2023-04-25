import os

DATA_DIR = "/home/ec2-user/data/extracted-2.1/"
DATA_IMAGE_DIR = DATA_DIR+"screenshot"
CLASS_LIST = ["area", "bar", "brush", "circular", "heatmap", "horizontal", "line", "linear", "point", "rect", "rule", "text", "triangleBottom", "triangleLeft", "triangleRight", "vertical", "withinLink"]
YOLOV7_IMAGE_DIR = "/home/ec2-user/data/model/extracted-2.1/"

def get_all_filenames(image_dir):
    images = os.listdir(image_dir)
    filenames = [os.path.splitext(im)[0] for im in images]
    return filenames

ALL_FILENAMES = get_all_filenames(DATA_IMAGE_DIR)

def generate_split(filenames, fold=5, seed=42):
    