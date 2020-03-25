# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2
import imutils
from subprocess import call
# File that I made where I implemented barcode lookup
from barcodelookup import lookup
# call(["set", "GOOGLE_APPLICATION_CREDENTIALS=C:\\Users\\rmisr\\Downloads\\LogoDetection-4f4b8a3b6759.json"])

# from picamera import PiCamera
# from time import sleep

# camera = PiCamera()

# camera.start_preview()
# sleep(1)
# camera.stop_preview()

# construct the argument psarser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to input image")
args = vars(ap.parse_args())

# load the input image
image = cv2.imread(args["image"])

pantryfoods = []

# find the barcodes in the image and decode each of the barcodes
barcodes = pyzbar.decode(image)
# print("hello")
# loop over the detected barcodes
print("----- BARCODE DETECTION -----")
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
    # barcodeData = barcodeData[1:]
    productname = lookup(barcodeData)
    text = "{} ({})".format(productname, barcodeData)
    cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
        0.5, (0, 0, 255), 2)
    #print(productname)
    # print the barcode type and data to the terminal
    pantryfoods.append(barcode)
    print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
for product in pantryfoods:
    if product not in barcodes:
        print("LOST " + product)
# show the output image
# print("hello1")
print()

print("----- LOGO DETECTION -----")

def detect_logos(path):
    """Detects logos in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.logo_detection(image=image)
    logos = response.logo_annotations

    for logo in logos:
        print(logo.description)

def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

# implicit()

cv2.imshow("Image", image)
detect_logos(args["image"])
cv2.waitKey(0)
