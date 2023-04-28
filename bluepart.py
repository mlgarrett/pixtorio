import cv2
import json
import zlib
import numpy
import base64

def scale_image(source, scale_percent):
	# scale the image
	# scale_percent = 0.10 # percent of original size
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

	# define criteria tuple and apply kmeans()
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

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
	res = center[label.flatten()]
	res2 = res.reshape((resized_image.shape))

	# for each pixel in the image, classify the color
		# create an equal-dimension "image" with the classifications at each pixel

	# initialize the blueprint dictionary
	bp = {"blueprint": {"tiles": [], "item": "blueprint"}}

	# for each pixel in the classified "image", add a tile to the blueprint
	# dictionary using the classification item ids with the associated position
	for i, row in enumerate(pixel_ids):
		for j, pixel in enumerate(row):
			# construct the dictionary entry
			entry = {"position": {"x": j, "y": i}, "name": pixel}
			bp["blueprint"]["tiles"].append(entry)
			# print(f'{e_counter}:({i},{j}): {pixel}')

	# console.print_json(json.dumps(bp))

	# encode the json dict to a byte string
	bp = str.encode(json.dumps(bp))

	# compress the byte string with zlib
	bp = zlib.compress(bp, level=9)

	# encode the compressed byte string to base64
	bp = base64.b64encode(bp)

	# push a zero version byte onto the front
	bp = b'0' + bp

	# the blueprint string is formed!
	# it is a byte string
	return bp
