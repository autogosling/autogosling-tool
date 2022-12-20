from flask import Flask, request, Response, jsonify
import itertools
from flask_cors import CORS
import numpy as np
# import yolov4
from PIL import Image
import json
from image_helper import draw_bounding_boxes, get_true_labelled_image
from yolov7_demo import predict
import base64
from io import BytesIO
from assemble import construct_spec

app = Flask(__name__)
CORS(app)

@app.route('/',methods=["GET"])
def main_route():
    return "Hello! This is the main route."

def pil2datauri(img):
    #converts PIL image to datauri
    data = BytesIO()
    img.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,'+data64.decode('utf-8')

'''
def perform_inference(pil_image):
    # this is a placeholder code. it currently returns the width and height of the image, but it should later be adapted to return the appropriate specs.
    width, height = pil_image.size
    boxes, classes, scores, annotated_img = predict(pil_image)
    return {"boxes" : boxes, "classes" : classes,"scores" : scores, "width" : width, "height" : height, "image" : pil2datauri(annotated_img)}
'''

@app.route('/viz_analysis',methods=["POST"])
def viz_analysis():
    image = request.files['image']
    # json_labels = json.load(request.files['json'])
    pil_image = Image.open(image)
    if not pil_image.mode == 'RGB':
        pil_image = pil_image.convert('RGB')
    shape_img, prop_img, shape_info, prop_info = predict(pil_image)
    # labelled_true_image = get_true_labelled_image(pil_image,json_labels)
    # tracks_info = # Load actual info 
    '''
    Example format: EX_TRACK_INFO = [
        {'x': 0, 'y': 0, 'width': 400, 'height': 430, 'layout': 'linear', 'mark': 'bar'}, 
        {'x': 0, 'y': 450, 'width': 400, 'height': 430, 'layout': 'linear', 'mark': 'line'}, 
        {'x': 410, 'y': 0, 'width': 400, 'height': 880, 'layout': 'linear', 'mark': 'point'}, 
        {'x': 0, 'y': 890, 'width': 800, 'height': 210, 'layout': 'linear', 'mark': 'area'}, 
        {'x': 0, 'y': 1100, 'width': 800, 'height': 210, 'layout': 'linear', 'mark': 'line'}]
    '''
    def parse_list(info_tuple):
        name,x0,y0,x1,y1,cls_id,score = info_tuple
        mydict = {'x' : x0, 'y' : y0, 'width' : x1-x0, 'height' : y1-y0, 'class' : name, 'score' : score}
        return mydict

    def has_iou(item1,item2,thresh=0.98):
        x0, y0, x1, y1 = item1['x'], item1['y'], item1['x'] + item1['width'], item1['y'] + item1['height']
        x2_0, y2_0, x2_1, y2_1 = item2['x'], item2['y'], item2['x'] + item2['width'], item2['y'] + item2['height']
        inner_x0 = max(x0,x2_0)
        inner_y0 = max(y0,y2_0)

        inner_x1 = min(x1,x2_1)
        inner_y1 = min(y1,y2_1)
        if inner_x0 < inner_x1 and inner_y0 < inner_y1:
            inner_area = (inner_y1 - inner_y0) * (inner_x1 - inner_x0)
            original_area = (x1-x0) * (y1 - y0)
            original_area2 = (x2_1-x2_0) * (y2_1 - y2_0)
            total_area = original_area + original_area2 - inner_area
            if inner_area / total_area > thresh:
                # merge the two bounding boxes!
                return True
        else:
            return False
    
    # for layout, choose the one with highest score
    # for marks, output those that are > than a certain confidence score
    # If only one mark in the bounding box: {'x': 0, 'y': 1100, 'width': 800, 'height': 210, 'layout': 'linear', 'mark': 'line'}
    # If multiple marks in the bounding box: {'x': 0, 'y': 1100, 'width': 800, 'height': 210, 'layout': 'linear', 'mark': ['rect', 'brush']}
    # TODO: Add orientation  {'x': 0, 'y': 1100, 'width': 800, 'height': 210, 'layout': 'linear', 'mark': ['rect', 'brush'], 'orientation': 'vertical'}

    def helper_cluster_similar_boxes(box,clusters):
        new_boxes = []
        found_box = False
        for cluster in clusters:
            copy_cluster = cluster.copy()
            if has_iou(cluster[0],box):
                found_box = True
                copy_cluster.append(box)
            new_boxes.append(copy_cluster)
        if not found_box:
            new_boxes.append([box])
        return new_boxes

    def cluster_similar_boxes(boxes):
        clusters = []
        for box in boxes:
            clusters = helper_cluster_similar_boxes(box,clusters)
        return clusters
    
    # Selects all labels from a given category that have a confidence score that is greater than a certain threshold
    def merge_identical_boxes(all_boxes,threshold=0.9):
        clusters = cluster_similar_boxes(all_boxes)
        def merge_labels(boxes):
            initial_obj = boxes[0].copy()
            all_classes = [box['class'] for box in boxes if box['score'] > threshold]
            if len(all_classes) == 1:
                initial_obj['class'] = all_classes[0]
            else:
                initial_obj['class'] = all_classes
            return initial_obj
        return [merge_labels(cluster) for cluster in clusters]

    # Selects only the best layout from similar bounding boxes
    def select_best_from_identical_boxes(all_boxes):
        clusters = cluster_similar_boxes(all_boxes)
        def merge_cluster(cluster):
            return max([box for box in cluster],key=lambda el: el['score'])
        return [merge_cluster(cluster) for cluster in clusters]

    def merge_parsed_list(shape_list,prop_list):
        merged_list = []
        for item1, item2 in itertools.product(shape_list,prop_list):
            if has_iou(item1,item2):
                new_item = {'x' : float(item1['x']), 'y' : float(item1['y']), 'width' : float(item1['width']), 'height' : float(item1['height']), 'layout' : item1['class'], 'mark' : item2['class'], 'score' : item2['score']}
                merged_list.append(new_item)
        return merged_list
    shape_info_parsed = select_best_from_identical_boxes([parse_list(my_list) for my_list in shape_info])
    prop_info_parsed = merge_identical_boxes([parse_list(my_list) for my_list in prop_info])


    tracks_info = merge_parsed_list(shape_info_parsed,prop_info_parsed)
    print(tracks_info)

    # '''
    spec = construct_spec(tracks_info,"vertical")
    images = {
    #    "labelled_image" : labelled_true_image,
        "shape_image" : shape_img,
        "property_image" : prop_img,
    }
    response = {key:pil2datauri(val) for key, val in images.items()}
    response["spec"]= spec
    response["tracks_info"]= tracks_info
    return jsonify(response)
    # '''

print("running app!")
app.run(host="0.0.0.0",port=7777,debug=False)
