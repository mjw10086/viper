from flask import Flask, jsonify, request
import os
import json
from main_simple_lib import *

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), "static"), static_url_path='/static')


def handle_request():
    if 'image' not in request.files:
        raise Exception('No image part in the request')

    image = request.files['image']
    if image.filename == '':
        raise Exception('No selected image')

    query = request.form.get('query', '')
    image_path = os.path.join("./", "uploads", image.filename)

    image.save(image_path)

    return image_path, query


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ImagePatch):
            return {'url': obj.filePath}
        return json.JSONEncoder.default(self, obj)


@app.route('/', methods=['GET'])
def index():
    return "Hello World"

@app.route('/v1per', methods=['POST'])
def chatWithViper():
    try:
        image_path, query = handle_request()
    except Exception as e:
        return e.message, 400

    im = load_image(image_path)
    code = get_code(query)
    code, query_result, exe_result = execute_code_return_result(code, im, show_intermediate_steps=True)
    all_result = {"code": code, "final_result": query_result, "step_result": exe_result}

    result = json.dumps(all_result, cls=CustomJSONEncoder, indent=4)
    
    return result, 200


if __name__ == '__main__':
    app.run(debug=True, port=8080)
