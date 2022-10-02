from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from PIL import Image

app = Flask(__name__)
CORS(app)

@app.route('/',methods=["GET"])
def main_route():
    return "Hello! This is the main route."

def perform_inference(pil_image):
    # this is a placeholder code. it currently returns the width and height of the image, but it should later be adapted to return the appropriate specs.
    width, height = pil_image.size
    return {"width" : width, "height" : height}

@app.route('/viz_analysis',methods=["POST"])
def viz_analysis():
    image = request.files['image']
    pil_image = Image.open(image)
    results = perform_inference(pil_image)
    return jsonify(results)

print("running app!")
app.run(host="0.0.0.0",port=5001)