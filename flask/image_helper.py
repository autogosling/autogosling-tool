import PIL
from PIL import Image, ImageDraw, ImageColor
import numpy as np
import json

# YOLOv4 Bounding Boxes
def draw_bounding_boxes(im: PIL.Image, bboxes: np.ndarray, classes: np.ndarray,
                        scores: np.ndarray) -> PIL.Image:
    im = im.copy()
    num_classes = len(set(classes))
    class_to_color_id = {cls: i for i, cls in enumerate(set(classes))}

    colors = [PIL.ImageColor.getrgb(f'hsv({int(360 * x / num_classes)},100%,100%)') for x in range(num_classes)]

    draw = PIL.ImageDraw.Draw(im)

    for bbox, cls, score in zip(bboxes, classes, scores):
        color = colors[class_to_color_id[cls]]
        draw.rectangle((*bbox.astype(np.int64),), outline=color)

        text = f'{cls}: {int(100 * score)}%'
        text_w, text_h = draw.textsize(text)
        draw.rectangle((bbox[0], bbox[1], bbox[0] + text_w, bbox[1] + text_h), fill=color, outline=color)
        draw.text((bbox[0], bbox[1]), text, fill=(0, 0, 0))

    return im

CIR_KEYS = {"cx", "cy", "innerRadius", "outerRadius", "startAngle", "endAngle"}
BOX_KEYS = {"x", "y", "width", "height"}
# BOX_KEYS = {"x", "y", "width", "height"}

def adjust_angle(ang):
    return ang-90

def draw_rect(dr, box):
    box_info = [box["x"], box["y"],box["x"]+box["width"], box["y"]+box["height"]]
    dr.rectangle(box_info, outline="red", width=3)

def draw_circular(dr,box,width=3):
    dr.line([0,100,])
    inner_arc_bb = [box["cx"]-box["innerRadius"], box["cy"]-box["innerRadius"],box["cx"]+box["innerRadius"], box["cy"]+box["innerRadius"]]
    dr.arc(inner_arc_bb, adjust_angle(box["startAngle"]), adjust_angle(box["endAngle"]), fill="red", width=3)
    outer_arc_bb = [box["cx"]-box["outerRadius"], box["cy"]-box["outerRadius"],box["cx"]+box["outerRadius"], box["cy"]+box["outerRadius"]]
    dr.arc(outer_arc_bb, adjust_angle(box["startAngle"]), adjust_angle(box["endAngle"]), fill="red", width=3)
    edge_start_inner_x = box["cx"] + box["innerRadius"]*np.cos(np.deg2rad(adjust_angle(box["startAngle"])))
    edge_start_inner_y = box["cy"] + box["innerRadius"]*np.sin(np.deg2rad(adjust_angle(box["startAngle"])))
    edge_start_outer_x = box["cx"] + box["outerRadius"]*np.cos(np.deg2rad(adjust_angle(box["startAngle"])))
    edge_start_outer_y = box["cy"] + box["outerRadius"]*np.sin(np.deg2rad(adjust_angle(box["startAngle"])))
    dr.line([edge_start_inner_x,edge_start_inner_y,edge_start_outer_x,edge_start_outer_y], fill="red", width=width)
    edge_end_inner_x = box["cx"] + box["innerRadius"]*np.cos(np.deg2rad(adjust_angle(box["endAngle"])))
    edge_end_inner_y = box["cy"] + box["innerRadius"]*np.sin(np.deg2rad(adjust_angle(box["endAngle"])))
    edge_end_outer_x = box["cx"] + box["outerRadius"]*np.cos(np.deg2rad(adjust_angle(box["endAngle"])))
    edge_end_outer_y = box["cy"] + box["outerRadius"]*np.sin(np.deg2rad(adjust_angle(box["endAngle"])))
    dr.line([edge_end_inner_x,edge_end_inner_y,edge_end_outer_x,edge_end_outer_y], fill="red", width=width)

def get_true_labelled_image(im, box_data):
    draw = ImageDraw.Draw(im)
    for box in box_data:
        if box.keys() == BOX_KEYS:
            draw_rect(draw, box)
        elif box.keys() == CIR_KEYS:
            draw_circular(draw,box)
    return im            
