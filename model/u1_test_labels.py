'''
This is a utility script to count the total occurence of labels in the dataset generated after a3_generate_yolov7.py
'''
from os.path import join as pjoin
from collections import Counter
import os


def load_txt(fn_path):
    with open(fn_path,"r") as f:
        return [line for line in f.read().split('\n') if len(line) > 1]
classes = load_txt("data/class_list.txt")
def print_stats(complete_path,mode):
    count = Counter()
    for filename in os.listdir(complete_path):
        complete_fn = pjoin(complete_path,filename)
        lines = load_txt(complete_fn)
        unique_classes = [line.split(" ")[0] for line in lines]
        count.update(unique_classes)
    
    stats = '\n'.join([f"{classes[int(val)]} ({val}): {count}"for val, count in count.most_common(100)])
    print("-"*50)
    print(mode)
    print(stats)
    print("-"*50)


data_dir = "data/splits/split-42-0.2/yolov7-42-0.2/labels"
for mode in os.listdir(data_dir):
    complete_path = pjoin(data_dir,mode)
    print_stats(complete_path,mode)
