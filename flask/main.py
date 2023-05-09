from flask import Flask, request, Response, jsonify
import itertools
from flask_cors import CORS
import numpy as np
# import yolov4
from PIL import Image
import json
from image_helper import draw_bounding_boxes, get_true_labelled_image
from util import parse_list,has_iou,helper_cluster_similar_boxes,cluster_similar_boxes,merge_identical_boxes,select_best_from_identical_boxes,merge_parsed_list
from yolov7_demo import predict
import base64
from io import BytesIO
from assemble import construct_spec, clean_track_info, add_track, remove_last_track
from finder import find_matching_files
import numpy as np
import gostalk

app = Flask(__name__)
CORS(app)

def rank_tracks(tracks):
    return list(sorted(tracks,key=lambda el: (el['x'], el['y'])))

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

@app.route('/true_viz_analysis',methods=["POST"])
def true_viz_analysis():
    image = request.files['image']
    pil_image = Image.open(image)
    if not pil_image.mode == 'RGB':
        pil_image = pil_image.convert('RGB')
    filename = request.files['image'].filename.split(".")[0]
    true_data = find_matching_files(filename)
    response = {}
    if true_data is not None:
        true_ss, true_tracks_info = true_data
        true_tracks_info = rank_tracks(true_tracks_info)
        response['image'] = pil2datauri(true_ss)
        response['tracks_info'] = true_tracks_info
        response['spec'] = construct_spec(true_tracks_info,"vertical")
        width, height = true_ss.size
        response["width"] = width
        response["height"] = height
    return jsonify(response)


def add_title(e):
    e[1]["title"] = str(e[0]+1)
    return e[1]
    
@app.route('/viz_analysis',methods=["POST"])
def viz_analysis():
    if (request.form["predict"] == "True"):
        print("Needs prediction!")
    elif ("gostalk_question" in request.form.keys()):
        question = request.form["gostalk_question"]
        print(question)
        print(str(request.form["spec"]))
        bot = gostalk.GosTalk_ChatGPT(template_chart=request.form["spec"])
        answer = bot.ask(question)
        response = {"spec": json.loads(answer[1]),
                    "explain":answer[0]}
        return jsonify(response)
    else:
        def format_tracks_info(track):
            for key, val in track.items():
                if key not in ["x", "y", "width", "height"]:
                    if type(val) is not list:
                        track[key] = [val]
            return track
        print("Just update!")
        tracks_info = json.loads(request.form["track_info"])
        tracks_info = list(map(format_tracks_info, tracks_info))
        tracks_info = list(map(clean_track_info, tracks_info))
        response = {}
        if "append" in request.form.keys() and request.form["append"] == "True":
            tracks_info = add_track(tracks_info)
        elif "delete" in request.form.keys() and request.form["delete"] == "True":
            selected = json.loads(request.form["selected"])
            if len(selected) > 0:
                tracks_info = [tracks_info[i] for i in range(len(tracks_info)) if not selected[i]]
        response["tracks_info"]= tracks_info
        if len(tracks_info)>0:
            with_title_tracks_info = list(map(add_title, enumerate(tracks_info)))
            temp_spec = construct_spec(with_title_tracks_info,"vertical")
            if "views" not in temp_spec:
                temp_spec = {"views": [temp_spec]}
            response["spec"] = temp_spec        
        return jsonify(response)
    image = request.files['image']
    # json_labels = json.load(request.files['json'])
    pil_image = Image.open(image)
    if not pil_image.mode == 'RGB':
        pil_image = pil_image.convert('RGB')
    RESIZE_WIDTH = 600
    RESIZE_HEIGHT = int(pil_image.size[1]*RESIZE_WIDTH/pil_image.size[0])
    pil_image = pil_image.resize((RESIZE_WIDTH,RESIZE_HEIGHT))
    #THUMBNAIL_SIZE = (640,640)
    #pil_image.thumbnail(THUMBNAIL_SIZE)
    # print(pil_image.size)
    shape_img, _, shape_info, prop_info = predict(pil_image)
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
    #print(shape_info)
    shape_info_parsed = select_best_from_identical_boxes([parse_list(my_list) for my_list in shape_info])
    #print("shape_info", shape_info)
    #print("prop_info", prop_info)
    #prop_info.extend(shape_info)

    prop_info_parsed = merge_identical_boxes([parse_list(my_list) for my_list in prop_info])
    print("prop_info_parsed",prop_info_parsed)
    print("shape_info_parsed",shape_info_parsed)


    def add_orientation(info):
        new_obj = info.copy()
        orientation_set = {"horizontal","vertical"}
        new_obj['orientation'] = [el for el in info['mark'] if el in orientation_set]
        if len(new_obj['orientation']) == 0:
            new_obj['orientation'] = ['horizontal']
        new_obj['mark'] = [el for el in info['mark'] if el not in orientation_set]
        return new_obj
    raw_tracks_info = merge_parsed_list(shape_info_parsed,prop_info_parsed)
    print("raw_tracks_info",raw_tracks_info)
    tracks_info = [add_orientation(info) for info in raw_tracks_info]
    tracks_info = [track_info for track_info in tracks_info if len(track_info['mark']) > 0]
    tracks_info = rank_tracks(tracks_info)
    # import ipdb; ipdb.set_trace()
    print(tracks_info)

    # '''
    images = {
        "image" : shape_img,
    }
    width, height = shape_img.size
    response = {key:pil2datauri(val) for key, val in images.items()}
    # response["spec"]= spec
    if len(tracks_info) > 0:
        tracks_info = list(map(clean_track_info, tracks_info))
        tracks_info = sorted(tracks_info, key=lambda x: (x["y"],x["x"],))
        with_title_tracks_info = list(map(add_title, enumerate(tracks_info)))
        temp_spec = construct_spec(with_title_tracks_info,"vertical")
        if "views" not in temp_spec:
            temp_spec = {"views": [temp_spec]}
        response["spec"] = temp_spec 
    #print(json.dumps(response["spec"], indent=2))
    response["tracks_info"]= tracks_info
    response["width"] = width
    response["height"] = height
    return jsonify(response)
    # '''


print("running app!")
app.run(host="0.0.0.0",port=7777,debug=False)
