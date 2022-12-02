from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import numpy as np
# import yolov4
from PIL import Image
import json
from image_helper import draw_bounding_boxes, get_true_labelled_image
from yolov7_demo import predict
import base64
from io import BytesIO
from assemble import construct_spec, EXAMPLE_FILENAME, read_info, create_filenames

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

def perform_inference(pil_image):
    # this is a placeholder code. it currently returns the width and height of the image, but it should later be adapted to return the appropriate specs.
    width, height = pil_image.size
    boxes, classes, scores, annotated_img = predict(pil_image)
    return {"boxes" : boxes, "classes" : classes,"scores" : scores, "width" : width, "height" : height, "image" : pil2datauri(annotated_img)}


@app.route('/viz_analysis',methods=["POST"])
def viz_analysis():
    image = request.files['image']
    json_labels = json.load(request.files['json'])
    pil_image = Image.open(image)
    if not pil_image.mode == 'RGB':
        pil_image = pil_image.convert('RGB')
    shape_img, prop_img = predict(pil_image)
    labelled_true_image = get_true_labelled_image(pil_image,json_labels)
    # tracks_info = # Load actual info
    tracks_info = read_info(create_filenames(EXAMPLE_FILENAME))
    spec = construct_spec(tracks_info,"vertical")
    images = {
        "labelled_image" : labelled_true_image,
        "shape_image" : shape_img,
        "property_image" : prop_img,
    }
    response = {key:pil2datauri(val) for key, val in images.items()}
    response["spec"]= spec
    response["tracks_info"]= tracks_info
    return jsonify(response)


print("running app!")
app.run(host="0.0.0.0",port=5031,debug=False)
