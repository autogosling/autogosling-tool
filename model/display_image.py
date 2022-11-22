import os
import random
from os.path import join as pjoin
import PIL
import PIL.ImageDraw
from PIL import Image


def load_lines(fn):
    with open(fn,"r") as f:
        lines =  f.read().split('\n')
        return [line for line in lines if len(line) > 1]

class_list_lines = load_lines("data/class_list-backup.txt")
def convert_to_bboxes(label_txt,full_w,full_h):
    lines = load_lines(label_txt)
    def parse_line(line):
        cls_id, c_x, c_y, w, h = line.split()
        c_x = float(c_x)
        c_y = float(c_y)
        w = float(w)
        h = float(h)

        c_x *= full_w
        w *= full_w
        c_y *= full_h
        h *= full_h

        return class_list_lines[int(cls_id)], c_x- w/2, c_y - h/2, c_x + w/2, c_y + h/2
    parsed_lines = list(map(parse_line,lines))
    return parsed_lines


data_dir = "data/splits/split-42-0.2/yolov7-42-0.2-backup/"
mode = 'test'
images_dir = pjoin(data_dir,'images',mode)
labels_dir = pjoin(data_dir,'labels',mode)



def draw_bbox(image_path,bboxes):
    im = Image.open(image_path)
    im = im.copy()
    draw = PIL.ImageDraw.Draw(im)
    for class_name, x0, y0, x1, y1 in bboxes:
        bbox = x0,y0,x1,y1
        draw.rectangle((x0,y0,x1,y1),outline="blue")
        text = class_name
        text_w, text_h = draw.textsize(text)
        text_x = bbox[0] + int(random.random()*(bbox[2]-bbox[1]))
        draw.rectangle((text_x, bbox[1], text_x + text_w, bbox[1] + text_h), fill="blue", outline="blue")
        draw.text((text_x, bbox[1]), text, fill=(0, 0, 0))
    return im

def do_all(image_path,label_path):
    full_w, full_h = Image.open(image_path).size
    bboxes = convert_to_bboxes(label_path,full_w,full_h)
    im = draw_bbox(image_path,bboxes)
    im.show()

stem = os.listdir(images_dir)[0].split(".")[0]
img = pjoin(images_dir,os.listdir(images_dir)[0])
label_txt = pjoin(labels_dir,stem+".txt")
do_all(img,label_txt)
print(stem)
fn = "data/splits/split-42-0.2/test/marks/"+stem+".json"
with open(fn,"r") as f:
    print(f.read())