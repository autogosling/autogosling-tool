# Generate a list of all unique labels

import os
from os.path import join as pjoin
import json
import itertools
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
    return list(sorted(class_vocab_set))

def create_vocab(marks_dir,layouts_dir):
    marks_list = update_class_vocab(set(),marks_dir)
    marks_list.remove("header")
    layouts_list = update_class_vocab(set(),layouts_dir)
    class_list = [f"{layout_name}-{mark_name}" for layout_name, mark_name in itertools.product(layouts_list,marks_list)]
    mapping_dir = {class_name : i for i,class_name in enumerate(class_list)}
    with open("data/class_mapping.json","w") as f:
        f.write(json.dumps(mapping_dir))

    with open("data/class_list.txt","w") as f:
        f.write('\n'.join(class_list))
    with open("data/class_list.json","w") as f:
        f.write(json.dumps(class_list))

if __name__ == "__main__":
    create_vocab(marks_dir,layouts_dir)