'''
Generates a list of all unique labels

Output: 
class_category_list.json: 
class_list.json
class_list.txt
class_mapping.json
'''

import os
from os.path import join as pjoin
import json
from a0_config import split_config, CLASS_FOLDERS, CLASS_FOLDER_NAMES

class_vocab_set = set()

def update_class_vocab(class_vocab_set,directory):
    for fn in os.listdir(directory):
        complete_path = pjoin(directory,fn)
        data = []
        with open(complete_path,"r") as f:
            data = json.load(f)
        data_strs = [str(el) for el in data if el is not None]
        class_vocab_set.update(data_strs)
    return list(sorted(class_vocab_set))

def create_vocab(categories,dirs):
    category_dict = {}
    for dir_category, dir in zip(categories,dirs):
        class_list = update_class_vocab(set(),dir)
        category_dict[dir_category] = class_list
    class_set = {value for list_value in category_dict.values() for value in list_value}
    class_list = list(sorted(class_set))
    mapping_dir = {class_name : i for i,class_name in enumerate(sorted(class_set))}
    
    with open("data/class_mapping.json","w") as f:
        f.write(json.dumps(mapping_dir))

    with open("data/class_list.txt","w") as f:
        f.write('\n'.join(class_list))
    
    with open("data/class_list.json","w") as f:
        f.write(json.dumps(class_list))
    
    with open("data/class_category_list.json","w") as f:
        f.write(json.dumps(category_dict))

if __name__ == "__main__":
    folders_dirs = [split_config[folder_name+"_folder"] for folder_name in CLASS_FOLDER_NAMES]
    create_vocab(CLASS_FOLDER_NAMES,folders_dirs)