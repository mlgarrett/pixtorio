import os
import cv2
import json
import zlib
import numpy
import base64
import secrets
from sklearn import cluster

def scale_image(source, scale_percent):
	# scale the image
	width = int(source.shape[1] * scale_percent)
	height = int(source.shape[0] * scale_percent)
	dim = (width, height)
	  
	# resize image
	resized = cv2.resize(source, dim, interpolation = cv2.INTER_AREA)

	return resized

def construct_blueprint(resized_image, palette):
	# reshape image
	Z = resized_image.reshape((-1,3))

	# convert to numpy.float32
	Z = numpy.float32(Z)

	# define how many colors (clusters) to use
	K = len(palette)

	kmeans_cluster = cluster.MiniBatchKMeans(n_clusters=K, init='k-means++', random_state=0, batch_size=K, max_iter=1, n_init='auto')
	kmeans_cluster.fit(Z)

	center = kmeans_cluster.cluster_centers_
	label = kmeans_cluster.labels_

	# define criteria tuple and apply kmeans()
	# criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5, 1.0)
	# ret, label, center = cv2.kmeans(Z, K, None, criteria, 5, cv2.KMEANS_PP_CENTERS)

	# this would sort the centers by their means
	# center[numpy.mean(center, axis=1).argsort()]

	# center now contains K RGB color values as a nested list

	# reshape the labels from kmeans back to the shape of the resized_image image
	labs = label.reshape((resized_image.shape[0], resized_image.shape[1]))
	# labs now contains a color classification integer for each pixel

	pixel_ids = []
	for row in labs:
		pixel_ids.append([palette[lab] for lab in row])
	pixel_ids = numpy.array(pixel_ids)
	# pixel_ids now contains the item ids from the palette for each pixel

	# Now convert back into uint8, and make downsampled image
	center = numpy.uint8(center)
	flat_centers = center[label.flatten()]
	res = flat_centers.reshape((resized_image.shape))

	# read each relevant sprite file from the palette
	sprites = numpy.array([scale_image(cv2.imread(os.path.join('sprites', t+'.png')), 0.05) for t in palette])

	# construct the rows of the preview image by hstack-ing the sprites
	preview_rows = []
	for row in labs:
		preview_rows.append(numpy.hstack([sprites[lab] for lab in row]))
	preview_rows = numpy.array(preview_rows)

	# produce final preview image by vstack-ing the rows
	preview = numpy.vstack([row for row in preview_rows])
	prev_width = preview.shape[1]
	prev_height = preview.shape[0]

	new_preview_width = 400
	ratio = new_preview_width / prev_width
	new_preview_height = int(prev_height*ratio)

	dimensions = (new_preview_width, new_preview_height)
	resized_preview = cv2.resize(preview, dimensions, interpolation=cv2.INTER_LINEAR)

	# save the preview image with a unique filename into the static previews
	# folder

	preview_path = os.path.join('static', 'preview', secrets.token_hex(4)+'.png')
	cv2.imwrite(preview_path, resized_preview)

	with open(preview_path, 'rb') as preview_file:
		encoded_preview = base64.encodebytes(preview_file.read())
	encoded_preview = encoded_preview.decode('utf-8')

	# delete the preview image
	os.remove(preview_path)

	# initialize the blueprint dictionary
	bp = {"blueprint": {"tiles": [], "item": "blueprint"}}

	# for each pixel in the classified "image", add a tile to the blueprint
	# dictionary using the classification item ids with the associated position
	for i, row in enumerate(pixel_ids):
		for j, pixel in enumerate(row):
			# construct the dictionary entry
			entry = {"position": {"x": j, "y": i}, "name": pixel}
			bp["blueprint"]["tiles"].append(entry)

	# encode the json dict to a byte string
	bp = str.encode(json.dumps(bp))

	# compress the byte string with zlib
	bp = zlib.compress(bp, level=9)

	# encode the compressed byte string to base64
	bp = base64.b64encode(bp)

	# push a zero version byte onto the front
	bp = b'0' + bp

	bp = bp.decode('utf-8')

	# the blueprint string is formed!
	# it is a byte string

	# response json contains the bp string and the preview image encoded in b64
	response = {'bp_string': bp, 'preview': encoded_preview}
	response = json.dumps(response)

	return response
