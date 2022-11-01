'''
The script data-conversion.py converts our dataset into the specific yolo format as follows:  

images/00001.png x1,y1,x2,y2,class_id x1,y1,x2,y2,class_id x1,y1,x2,y2,class_id x1,y1,x2,y2,class_id 
images/00002.png x1,y1,x2,y2,class_id x1,y1,x2,y2,class_id 

where x1, y1, x2, y2 are the coordinates of the bounding boxes


Data path: 
test: model/data/splits/split-42-0.2/test
train: model/data/splits/split-42-0.2/train

images: images/
bounding boxes: bounding_box

if rectangular, 
x1 = x
y1 = y
x2 = x+width
y2 = y+height

if circular,
x1 = cx - outer_radius
y1 = cy - outer_radius
x2 = cx + outer_radius
y2 = cy + outer_radius

label: label
'''

import json
import os
from pathlib import Path

def bbox_label_string(bbox_entry, label_entry):
    if label_entry == None:
        return ""
    
    output = ""
    if "cx" in bbox_entry:
        cx = bbox_entry['cx']
        cy = bbox_entry['cy']
        outer_radius = bbox_entry['outerRadius']

        x1 = cx - outer_radius
        y1 = cy - outer_radius
        x2 = cx + outer_radius
        y2 = cy + outer_radius
        
    else:
        x1 = bbox_entry['x']
        y1 = bbox_entry['y']
        x2 = x1 + bbox_entry['width']
        y2 = y1 + bbox_entry['height']

    output = ",".join([str(x1), str(y1), str(x2), str(y2)])

    return " " + ",".join([output, label_entry])
    

def generate_yolo_txt(path, mode):
    
    with open(os.path.join(path, mode + '_processed.txt'), 'w') as f:

        for file in os.listdir(path + '/images'):    
            
            # Image name
            output = ""
            output += "images/" + file

            # Bounding boxes and labels
            bbox_path = os.path.join(path, 'bbox', Path(file).stem + '.json')
            label_path = os.path.join(path, 'label', Path(file).stem + '.json')

            bbox_file = open(bbox_path)
            bbox = json.load(bbox_file)
        
            label_file = open(label_path)
            label = json.load(label_file)

            # assert len(bbox) == len(label)

            for i in range(len(bbox)):
                output += bbox_label_string(bbox[i], label[i])

            f.write(output + "\n")


if __name__ == "__main__":
    path = 'data/splits/split-42-0.2/'
    generate_yolo_txt(os.path.join(path, 'train'), 'train')
    generate_yolo_txt(os.path.join(path, 'test'), 'test')