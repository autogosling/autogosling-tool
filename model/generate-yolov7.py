'''
The script generate-yolov7.py converts our initial data already splitted in train/[label or images or bbox] and test/[label or images or bbox] into a yolov7/images/train and yolov7/images/labels:

split-42-0.2
- yolov7
-- images
--- train
---- trainimage01.png
---- ...
--- test
---- testimage01.png
---- ...
-- labels
--- train
---- train01.txt
---- ...
--- test
---- test01.txt
---- ...

GIVEN

└───train
    │  bbox
    |  └─── example1.json
    |  └─── ...
    |  images
    |  └─── example1.png
    |  └─── ...
    |  label
    |  └─── example1.json
    |  └─── ...
└───test (same structure as train folder)
    |  bbox
    |  images
    |  label
'''

import os
from pathlib import Path
import json
from shutil import copyfile
# from sklearn.model_selection import train_test_split
import numpy as np
from PIL import Image
from os.path import join as pjoin

SEED = 42
TEST_SIZE = 0.2

np.random.seed(SEED)

yolov7_configuration = {
    "split_folder" : "data/splits/split-42-0.2",
    "output_folder" : "data/splits/split-42-0.2/yolov7-42-0.2"
}

IMAGES = "images"
BBOX = "bbox"
LABELS = "labels"
def make_folders_if_not_exist(folder_path):
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

def copy_images(split_folder,output_folder,mode):
    src_images = pjoin(split_folder,mode,IMAGES)
    dest_images = pjoin(output_folder,IMAGES,mode)
    make_folders_if_not_exist(dest_images)
    size_dict = {}

    for img_path in os.listdir(src_images):
        complete_src_img_path = pjoin(src_images,img_path)
        complete_dest_img_path = pjoin(dest_images,img_path)
        full_width, full_height = Image.open(complete_src_img_path).size
        copyfile(complete_src_img_path,complete_dest_img_path)
        stem = img_path.split(".")[0]
        size_dict[stem] = (full_width, full_height)
    return size_dict

def convert_txt(json_path,full_w,full_h):
    data = []
    with open(json_path,"r") as f:
        data = json.load(f)
    def parse_item(item):
        cx,cy,w,h = None, None, None, None
        category = 0
        if "width" in item: # then this is rectangular
            x,y,w,h = item["x"], item["y"], item['width'], item['height']
            cx, cy = x + w/2, y + h/2
            category = 0
        elif "outerRadius" in item: # then it is circular
            cx, cy = item['cx'], item['cy']
            w = h = item['outerRadius']
            category = 1
        else:
            return None
        cx /= full_w
        cy /= full_h
        w /= full_w
        h /= full_h
        all_strs = [str(el) for el in [category,cx,cy,w,h]]
        return ' '.join(all_strs)
        
    content = '\n'.join(set(filter(lambda el: el is not None,[parse_item(item) for item in data])))
    return content
    

def write_txt(fn,content):
    with open(fn,"w") as f:
        f.write(content)

def copy_and_convert_labels(split_folder,output_folder,mode,img_sizes):
    src_labels = pjoin(split_folder,mode,BBOX)
    dest_labels = pjoin(output_folder,LABELS,mode)
    make_folders_if_not_exist(dest_labels)

    for json_label_path in os.listdir(src_labels):
        complete_src_label_path = pjoin(src_labels,json_label_path)
        stem_path = json_label_path.split(".")[0]
        dest_end = stem_path + ".txt"
        full_w, full_h = img_sizes[stem_path]
        complete_dest_label_path = pjoin(dest_labels,dest_end)
        txt_content = convert_txt(complete_src_label_path, full_w, full_h)
        write_txt(complete_dest_label_path,txt_content)


def generate_yolov7_folder(split_folder,output_folder):
    # read through train path to extract and copy the images first
    train_img_sizes = copy_images(split_folder,output_folder,"train")
    copy_and_convert_labels(split_folder,output_folder,"train",train_img_sizes)

    test_img_sizes = copy_images(split_folder,output_folder,"test")
    copy_and_convert_labels(split_folder,output_folder,"test",test_img_sizes)

    valid_img_sizes = copy_images(split_folder,output_folder,"valid")
    copy_and_convert_labels(split_folder,output_folder,"valid",valid_img_sizes)


if __name__ == "__main__":
    generate_yolov7_folder(**yolov7_configuration)
    print(f"Finished generating yolov7 folder!")