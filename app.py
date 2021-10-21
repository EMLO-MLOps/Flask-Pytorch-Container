from flask import Flask, render_template, request, send_from_directory
from models import MobileNet
import os
from math import floor
from werkzeug.utils import secure_filename
from db import *


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'media/uploads'
app.config['DB_FOLDER'] = 'media/db'

if not os.path.isdir(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'],
                exist_ok=True)

if not os.path.isdir(app.config['DB_FOLDER']):
    os.makedirs(app.config['DB_FOLDER'],
                exist_ok=True)


model = MobileNet()

@app.route("/media/<path:path>")
def static_dir(path):
    return send_from_directory("media", path)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/infer', methods=['POST'])
def success():
    if request.method == 'POST':

        files = request.files.getlist('files[]')
        outputs = []

        json_file = init_json(app.config['DB_FOLDER'])


        for file in files:
            if file:
                file_name = secure_filename(file.filename)
                saveLocation = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
                file.save(saveLocation)


                inference, confidence = model.infer(saveLocation)
                # make a percentage with 2 decimal points
                confidence = floor(confidence * 10000) / 100

                output = {
                    "filename": file_name,
                    "confidence": confidence,
                    "inference": inference,
                    "saveLocation": saveLocation
                }
                outputs.append(output)


                json_file = update_json(json_file, output)


                previous_data = get_prev(json_file)
                previous_data = convert(previous_data)
                # respond with the inference
                print(previous_data)

        return render_template('inference.html',
                               prev = previous_data,
                               outputs = outputs)


if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port, debug=True)
