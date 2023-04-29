import os
import cv2
import json
import bluepart as bp
from flask import Flask, render_template, request, redirect, make_response, jsonify, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def welcome():
	return render_template('index.html')

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def generate_blueprint():
	if request.method == 'POST':
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

			# delete the uploaded file for cleanliness
			os.remove(filepath)

			# rescale the input image
			resized_image = bp.scale_image(og_image, scaling_factor)

			# produce the blueprint string (as bytes) and a preview image
			message = bp.construct_blueprint(resized_image, tiles)

			# form and send the response
			response = make_response(message, 200)
			response.mimetype = "text/plain"

			return response
		else:
			message = {"bp_string": 0}
			str.encode(json.dumps(message))
			response = make_response(message, 415)
			return response

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
	app.run(host='0.0.0.0')