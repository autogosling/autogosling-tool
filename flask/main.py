from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import numpy as np
import yolov4
from PIL import Image
import json
from image_helper import draw_bounding_boxes, get_true_labelled_image
import base64
from io import BytesIO
yo = yolov4.YOLOv4(num_classes=80)
yo.load_weights(weights_path=None)

app = Flask(__name__)
CORS(app)

@app.route('/',methods=["GET"])
def main_route():
    return "Hello! This is the main route."

def predict(yolo_model,image):
    boxes, classes, scores = yolo_model.predict(np.array(image))
    annotated_img = draw_bounding_boxes(image,boxes,classes,scores)
    return boxes.tolist(), classes.tolist(), scores.tolist(), annotated_img

def pil2datauri(img):
    #converts PIL image to datauri
    data = BytesIO()
    img.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,'+data64.decode('utf-8')

def perform_inference(pil_image):
    # this is a placeholder code. it currently returns the width and height of the image, but it should later be adapted to return the appropriate specs.
    width, height = pil_image.size
    boxes, classes, scores, annotated_img = predict(yo,pil_image)
    return {"boxes" : boxes, "classes" : classes,"scores" : scores, "width" : width, "height" : height, "image" : pil2datauri(annotated_img)}

@app.route('/viz_analysis',methods=["POST"])
def viz_analysis():
    image = request.files['image']
    json_labels = json.load(request.files['json'])
    pil_image = Image.open(image)
    results = perform_inference(pil_image)
    labelled_true_image = get_true_labelled_image(pil_image,json_labels)
    return jsonify({**results, "labelled_image" : pil2datauri(labelled_true_image)})

print("running app!")
app.run(host="0.0.0.0",port=5001)