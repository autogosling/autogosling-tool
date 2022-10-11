'''
The script generate-split.py generates a split of the following folder structure (given a seed of 42 and test_size of 20%)
split-42-0.2
- train
- - bbox
- - image
- - label
- test
- - bbox
- - image
- - label
'''
import os
from pathlib import Path
from shutil import copyfile
from sklearn.model_selection import train_test_split
from os.path import join as pjoin

SEED = 42
TEST_SIZE = 0.2

split_configuration = {
    "image_folder" : "data/image",
    "bbox_folder" : "data/bbox",
    "label_folder" : "data/label"
}

def extract_mapping_ids(folder_path):
    '''Returns a mapping dictionary that has the shape {`00001` : `train-images/00001.png`, `00002` : `train_images/00002.png`, ...}'''
    ids = {Path(filename).stem : os.path.join(folder_path,filename) for filename in os.listdir(folder_path)}
    return ids

def generate_folders(output_directory, mode):
    '''generates the 3 folders (image, bounding boxes, label) given a mode "train" or "test"'''
    folder_names = ["image", "bbox", "label"]
    all_folders = {
        # this join statement will makea folder called split-42-0.2/train/image for example
        folder_name : pjoin(output_directory,mode,folder_name) for folder_name in folder_names
    }
    for folder_path in all_folders.values():
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
    return all_folders

def copy_dataset(output_ids, output_folder):
    
    for sample_id in output_ids:
        copyfile()
    # todo

def create_split(image_folder,bbox_folder,label_folder):
    all_mapping_ids_set = {folder_name:extract_mapping_ids(folder_name) for folder_name in [image_folder,label_folder,bbox_folder]}
    all_ids = [set(mapping_id.keys()) for mapping_id in all_mapping_ids_set]
    common_ids = list(set.intersection(*all_ids))
    train_ids, test_ids = train_test_split(common_ids,random_state=SEED,test_size=TEST_SIZE)
    output_directory = f"split-{SEED}-{TEST_SIZE}"
    train_folders = generate_folders(output_directory,"train")
    test_folders = generate_folders(output_directory,"test")

    copy_dataset(train_ids,train_folders)
    copy_dataset(test_ids,test_folders)




