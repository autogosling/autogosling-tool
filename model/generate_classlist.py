# Generate a list of all unique labels

import os
from os.path import join as pjoin
import json
marks_dir = "data/marks"
layouts_dir = "data/layouts"

class_vocab_set = set()

def update_class_vocab(class_vocab_set,directory):
    for fn in os.listdir(directory):
        complete_path = pjoin(directory,fn)
        data = []
        with open(complete_path,"r") as f:
            data = json.load(f)
        data_strs = [str(el) for el in data if el is not None]
        class_vocab_set.update(data_strs)
    return class_vocab_set

def create_vocab(dirs):
    for dir in dirs:
        update_class_vocab(class_vocab_set,dir)
    class_list = list(sorted(class_vocab_set))
    mapping_dir = {class_name:i for i,class_name in enumerate(class_list)}
    with open("data/class_mapping.json","w") as f:
        f.write(json.dumps(mapping_dir))

    with open("data/class_list.txt","w") as f:
        f.write('\n'.join(class_list))

if __name__ == "__main__":
    create_vocab([marks_dir,layouts_dir])