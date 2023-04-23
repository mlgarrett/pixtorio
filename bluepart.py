import cv2
import json
import zlib
import base64
import numpy

from rich.console import Console

console = Console()

# define a "palette" which associates color classifications with item ids
palette = {0: "stone-path", 1: "concrete", 2: "refined-concrete", 3: "hazard-concrete-right", 4: "refined-hazard-concrete-left"}

# input an image (probably as ndarray)
og_image = cv2.imread('boker_crop.jpg')

# scale the image
scale_percent = 10 # percent of original size
width = int(og_image.shape[1] * scale_percent / 100)
height = int(og_image.shape[0] * scale_percent / 100)
dim = (width, height)
  
# resize image
resized = cv2.resize(og_image, dim, interpolation = cv2.INTER_AREA)

# reshape image
Z = resized.reshape((-1,3))

# convert to numpy.float32
Z = numpy.float32(Z)

# define how many colors (clusters) to use
K = len(palette)

# define criteria tuple and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# center now contains K RGB color values as a nested list

# reshape the labels from kmeans back to the shape of the resized image
labs = label.reshape((resized.shape[0], resized.shape[1]))

# labs now contains a color classification integer for each pixel

pixel_ids = []
for row in labs:
	pixel_ids.append([palette[lab] for lab in row])

pixel_ids = numpy.array(pixel_ids)

# pixel_ids now contains the item ids from the palette for each pixel

# Now convert back into uint8, and make downsampled image
center = numpy.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((resized.shape))

cv2.imwrite('output.jpg', res2)

# for each pixel in the image, classify the color
	# create an equal-dimension "image" with the classifications at each pixel

newBp = {"blueprint": {"entities": [{"entity_number": 1, "name": "wooden-chest", "position": {"x": 1, "y": 1}}], "item": "blueprint"}}

# initialize the blueprint dictionary
bp = {"blueprint": {"tiles": [], "item": "blueprint"}}

e_counter = 1
# for each pixel in the classified "image", add a tile to the blueprint
# dictionary using the classification item ids with the associated position
for i, row in enumerate(pixel_ids):
	for j, pixel in enumerate(row):
		# construct the dictionary entry
		entry = {"position": {"x": j, "y": i}, "name": pixel}
		bp["blueprint"]["tiles"].append(entry)
		# print(f'{e_counter}:({i},{j}): {pixel}')
		e_counter += 1

# console.print_json(json.dumps(bp))

# encode the json dict to a byte string
bp = str.encode(json.dumps(bp))

# compress the byte string with zlib
bp = zlib.compress(bp, level=9)

# encode the compressed byte string to base64
bp = base64.b64encode(bp)

# push a zero version byte onto the front
bp = b'0' + bp

# the blueprint string is formed
# it is a byte string
print(bp.decode('utf-8'))
