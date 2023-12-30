import os
import cv2
import json
import logging
import bluepart as bp
from logger import PixtorioLogger
from flask import Flask, render_template, request, redirect, make_response, jsonify, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

logger = PixtorioLogger()

@app.route('/')
def welcome():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def return_error():
    message = {"bp_string": 0}
    message = json.dumps(message)
    response = make_response(message, 415)
    response.mimetype = "text/plain"

    return response

@app.route('/', methods=['GET', 'POST'])
def generate_blueprint():
    if request.method == 'POST':
        # capture ip for the log file
        remote_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

        # the image file from the ui
        source_file = request.files['source']

        if source_file and allowed_file(source_file.filename):
            filename = secure_filename(source_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            source_file.save(filepath)

            # the scaling factor from the ui
            scaling_factor = float(request.form.get("scale"))

            # the selected tiles from the ui
            tiles = request.form.getlist('tiles')

            # read the image
            og_image = cv2.imread(filepath)

            # if we failed to read the image
            if og_image is None:
                os.remove(filepath)
                return return_error()

            # rescale the input image
            resized_image = bp.scale_image(og_image, scaling_factor)

            # produce the blueprint string (as bytes) and a preview image
            message = bp.construct_blueprint(resized_image, tiles)

            # form and send the response
            response = make_response(message, 200)
            response.mimetype = "text/plain"

            # delete the uploaded file for cleanliness
            os.remove(filepath)

            # write an info log record
            logger.log_message(remote_ip, logging.INFO)

            return response
        else:
            # write an error log record
            logger.log_message(remote_ip, logging.ERROR)

            return return_error()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
