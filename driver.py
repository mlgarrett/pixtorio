import os
import cv2
import bluepart as bp
from flask import Flask, render_template, request, redirect, make_response, jsonify
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
		source_file = request.files['source']
		# print(source_file)

		if source_file and allowed_file(source_file.filename):
			filename = secure_filename(source_file.filename)
			filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			source_file.save(filepath)
			# print(filepath)

		scaling_factor = float(request.form.get("scale"))
		# print(scaling_factor)

		tiles = request.form.getlist('tiles')
		# print(tiles)

		# read the image
		og_image = cv2.imread(filepath)

		# delete the uploaded file for cleanliness
		os.remove(filepath)

		# rescale the input image
		resized_image = bp.scale_image(og_image, scaling_factor)

		# produce the blueprint string (as bytes)
		bp_bytes = bp.construct_blueprint(resized_image, tiles)

		message = bp_bytes.decode('utf-8')
		response = make_response(message, 200)
		response.mimetype = "text/plain"

	return response
