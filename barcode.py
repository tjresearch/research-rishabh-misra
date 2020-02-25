# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2
from subprocess import call
from barcodelookup import lookup # File that I made where I implemented barcode lookup
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

# load the input image
image = cv2.imread(args["image"])
 
# find the barcodes in the image and decode each of the barcodes
barcodes = pyzbar.decode(image)
#print("hello")
# loop over the detected barcodes
for barcode in barcodes:
	# extract the bounding box location of the barcode and draw the
	# bounding box surrounding the barcode on the image
	(x, y, w, h) = barcode.rect
	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
 
	# the barcode data is a bytes object so if we want to draw it on
	# our output image we need to convert it to a string first
	barcodeData = barcode.data.decode("utf-8")
	barcodeType = barcode.type
 
	# draw the barcode data and barcode type on the image
	#barcodeData = barcodeData[1:]
	productname = lookup(barcodeData)
	text = "{} ({})".format(productname, barcodeData)
	cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 0, 255), 2)
	print(productname)
	# print the barcode type and data to the terminal

	print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

 
# show the output image
#print("hello1")
cv2.imshow("Image", image)
cv2.waitKey(0)