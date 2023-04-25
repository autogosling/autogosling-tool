'''
To match the yolov7 input format, this script converts our splitted dataset (e.g., train/[label or images or bbox], valid/[label or images or bbox] and test/[label or images or bbox]) into images/[train or valid or test] and labels/[train or valid or test]:
Additionally, it creates the labels txt files in the yolov7 format (label x1 x2 y1 y2) where x1 x2 y1 y2 are the 

split-42-0.2-0.1
└─── yolov7-42-0.2-0.1
     └─── images
     |    └─── train
     |    |     └─── trainimage01.png
     |    |     └─── ...
     |    └─── test
     |          └─── testimage01.png
     |          └─── ...
     └─── labels
          └─── train
          |     └─── train01.txt
          |     └─── ...
          └─── test
                └─── test01.txt
                └─── ...

GIVEN

└─── train
|    └─── bounding_box
|    |    └─── example1.json
|    |    └─── ...
|    └─── chart
|    |    └─── example1.json
|    |    └─── ...
|    └─── image (screenshot)
|    |    └─── example1.png
|    |    └─── ...
|    └─── layout
|    |    └─── example1.json
|    |    └─── ...
|    └─── orientation
|         └─── example1.json
|         └─── ...
└─── test (same structure as train folder)
└─── valid (same structure as train folder)
'''

import os
from pathlib import Path
import json
from shutil import copyfile
# from sklearn.model_selection import train_test_split
import numpy as np
from PIL import Image
from os.path import join as pjoin
from a0_config import IMAGE_FOLDER, BBOX_FOLDER, CLASS_FOLDERS, split_config, CLASS_FOLDER_NAMES, YOLOV7_LABELS, YOLOV7_IMAGES

yolov7_config = {
    "split_folder" : "data/splits/split-42-0.2-0.1",
    "output_folder" : "data/splits/split-42-0.2-0.1/yolov7-42-0.2-0.1"
}

IMAGES = Path(split_config[IMAGE_FOLDER]).name
BBOX = Path(split_config[BBOX_FOLDER]).name

def load_mapping(mapping_fn="data/class_mapping.json"):
    with open(mapping_fn,"r") as f:
        return json.load(f)

def to_indices(mylist):
    return {el:i for i,el in enumerate(mylist)}
CLASS_MAPPING = to_indices(["area", "bar", "betweenLink", "circular", "heatmap", "horizontal", "ideogram", "line", "linear", "point", "rect", "rule", "text", "triangleLeft", "triangleRight", "vertical", "withinLink"])

# CLASS_MAPPING = load_mapping()
def make_folders_if_not_exist(folder_path):
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

def copy_images(split_folder,output_folder,mode):
    src_images = pjoin(split_folder,mode,IMAGES)
    dest_images = pjoin(output_folder,YOLOV7_IMAGES,mode)
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

def get_class_ind(string):
    return CLASS_MAPPING.get(string,-1)

def convert_txt(json_path,classes, full_w,full_h):
    data = []
    with open(json_path,"r") as f:
        data = json.load(f)
    def parse_item(item,current_classes):
        cx,cy,w,h = None, None, None, None
        category = 0
        if "width" in item: # then this is rectangular
            x,y,w,h = item["x"], item["y"], item['width'], item['height']
            cx, cy = x + w/2, y + h/2
        elif "outerRadius" in item: # then it is circular
            cx, cy = item['cx'], item['cy']
            w = h = item['outerRadius']*2
        else:
            return None
        cx /= full_w
        cy /= full_h
        w /= full_w
        h /= full_h

        rest_data = ' '.join([str(el) for el in [cx,cy,w,h]])
        def encode_numerical(multihot):
            orig_num = 0
            for el in multihot:
                orig_num += 1 << el
            return orig_num

        def clean_dump(object):
            return int(4* encode_numerical(object[0]) + 2 * object[1] + 1 * object[2]) # Storing labels (e.g., mark 14, ) in the following format
        print(current_classes)
        return list({f"{i} {rest_data}" for i in current_classes})
    print(classes)
    nested_lists = filter(lambda el: el is not None,[parse_item(item,current_classes) for item,current_classes in zip(data,classes)])
    flattened_set = set([el for sublist in nested_lists for el in sublist])
    content = '\n'.join(flattened_set)
    return content
    

def write_txt(fn,content):
    with open(fn,"w") as f:
        f.write(content)

def flatten_list(mylist):
    for el in mylist:
        if type(el) == list:
            for new_el in flatten_list(el):
                yield new_el
        else:
            yield el

def read_classes(stem_path,split_folder,mode):

    def gather_classes_json(folder):
        folder_name = Path(split_config[folder+"_folder"]).name
        complete_path = pjoin(split_folder,mode,folder_name,stem_path+".json")
        classes = []
        with open(complete_path,"r") as f:
            classes = json.load(f)
        return classes
    
    def convert_mapping(els,name):
        if type(els) == list:
            return [CLASS_MAPPING[class_el] for class_el in els]
        else:
            return CLASS_MAPPING[els] # just a single element

    def convert_dict(class_list):
        return list(flatten_list([convert_mapping(subclass_list,name) for name, subclass_list in zip(CLASS_FOLDER_NAMES,class_list)]))
        # return [CLASS_MAPPING[class_el] for class_el in flatten_list(class_list)]
    
    all_classes = [gather_classes_json(folder) for folder in CLASS_FOLDER_NAMES]
    result =  [convert_dict(class_list) for class_list in zip(*all_classes)] 
    return result
    
        

def copy_and_convert_labels(split_folder,output_folder,mode,img_sizes):
    src_bbox_path = pjoin(split_folder,mode,BBOX)
    dest_labels = pjoin(output_folder,YOLOV7_LABELS,mode)
    make_folders_if_not_exist(dest_labels)
    total_not_found = 0
    total_found = 0
    for json_label_path in os.listdir(src_bbox_path):
        complete_src_bbox_path = pjoin(src_bbox_path,json_label_path)
        stem_path = json_label_path.split(".")[0]
        dest_end = stem_path + ".txt"
        if stem_path not in img_sizes:
            # print("Not found:",stem_path)
            total_not_found += 1
            continue
        if stem_path in img_sizes:
            # print("Found:", stem_path)
            total_found += 1
        full_w, full_h = img_sizes[stem_path]
        complete_dest_label_path = pjoin(dest_labels,dest_end)
        classes_content = read_classes(stem_path,split_folder,mode)
        txt_content = convert_txt(complete_src_bbox_path,classes_content, full_w, full_h)
        write_txt(complete_dest_label_path,txt_content)

    print(f"Mode: {mode}. Found: {total_found} Not Found:{total_not_found}")

def generate_yolov7_folder(yolov7_config):
    # read through train path to extract and copy the images first
    split_folder = yolov7_config['split_folder']
    output_folder = yolov7_config['output_folder']
    modes = ['train','test','valid']
    for mode in modes:
        img_sizes = copy_images(split_folder,output_folder,mode)
        copy_and_convert_labels(split_folder,output_folder,mode,img_sizes)


if __name__ == "__main__":
    generate_yolov7_folder(yolov7_config)
    print(f"Finished generating yolov7 folder at {yolov7_config['output_folder']}")
