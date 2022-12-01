'''
The script generate-split.py generates a split of the following folder structure (given a seed of 42 and test_size of 20%):

split-42-0.2
└───train
    │  bounding_box
    |  └─── example1.json
    |  └─── ...
    |  chart
    |  └─── example1.json
    |  └─── ...
    |  image
    |  └─── example1.png
    |  └─── ...
    |  layout
    |  └─── example1.json
    |  └─── ...
    |  mark
    |  └─── example1.json
    |  └─── ...
    |  orientation
    |  └─── example1.json
    |  └─── ...
└───test (same structure as train folder)
    |  bounding_box
    |  chart
    |  image
    |  layout
    |  mark
    |  orientation
'''
import os
from pathlib import Path
from shutil import copyfile
import numpy as np
from os.path import join as pjoin

# from sklearn.model_selection import train_test_split
from a0_config import split_config
from a0_config import SEED, TEST_SIZE, VALID_SIZE

# temporary fix until I fix my sklearn import
def train_test_split(common_ids,test_size=0.2):
    inds = np.arange(0,len(common_ids))
    np.random.shuffle(inds)
    test_ind = int(test_size * len(inds))
    return common_ids[test_ind:], common_ids[:test_ind]

def extract_mapping_ids(folder_path):
    '''Returns a mapping dictionary that has the shape {`00001` : `train-screenshots/00001.png`, `00002` : `train_screenshots/00002.png`, ...}'''
    ids = {Path(filename).stem : os.path.join(folder_path,filename) for filename in os.listdir(folder_path)}
    return ids

def generate_folders(output_directory, mode,split_config=split_config):
    '''Generates 6 folders (bounding boxes, chart, layouts, marks, orientations, screenshot) given a mode "train" or "test"'''
    # folder_names = ["images", "bbox", "layouts","marks"] # Use line below to generate folder names
    folder_names = list([Path(path).name for path in split_config.values()])
    all_folders = {
        # this join statement will make a folder called split-42-0.2/train/images for example
        folder_name : pjoin(output_directory,mode,folder_name) for folder_name in folder_names
    }
    for folder_path in all_folders.values():
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
    return all_folders

def copy_dataset(output_ids, output_folders,all_mappings_ids):
    for sample_id in output_ids: #output ids will be the ids in either the train or test folder
        for name, output_dir in output_folders.items(): 
            src_path = all_mappings_ids[name][sample_id]
            filename = Path(src_path).name
            output_path = pjoin(output_dir,filename)
            copyfile(src_path,output_path)

def create_split(split_config):
    # folder_paths = [image_folder, bbox_folder, layout_folder,mark_folder] # Use code below to generate folder paths and names
    # folder_names = ["images", "bbox", "label","marks"]
    folder_paths = list(split_config.values())
    folder_names = [Path(path).name for path in split_config.values()]
    all_mapping_ids_set = {folder_name:extract_mapping_ids(folder_path) for folder_name, folder_path in zip(folder_names, folder_paths)}
    all_ids = [set(mapping_id.keys()) for mapping_id in all_mapping_ids_set.values()]
    common_ids = list(set.intersection(*all_ids))
    common_ids = [id_string for id_string in common_ids if not id_string.startswith("gene_annotation")]
    train_ids, test_ids = train_test_split(common_ids,test_size=TEST_SIZE)
    train_ids, valid_ids = train_test_split(train_ids,test_size=VALID_SIZE)
    output_directory = f"data/splits/split-{SEED}-{TEST_SIZE}-{VALID_SIZE}"
    train_folders = generate_folders(output_directory,"train")
    valid_folders = generate_folders(output_directory,"valid")
    test_folders = generate_folders(output_directory,"test")
    copy_dataset(train_ids,train_folders,all_mapping_ids_set)
    copy_dataset(valid_ids,valid_folders,all_mapping_ids_set)
    copy_dataset(test_ids,test_folders,all_mapping_ids_set)

if __name__ == "__main__":
    create_split(split_config)
    # create_split(**split_configuration)
    print(f"Finished creating split of seed {SEED} and test_size {TEST_SIZE} and valid size {VALID_SIZE}")
    print(f"The data has been created at /data/splits/split-{SEED}-{TEST_SIZE}-{VALID_SIZE}")