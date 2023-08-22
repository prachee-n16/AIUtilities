import os
from PIL import Image, ImageFilter
import pytesseract
from pytesseract import Output
import numpy as np
import cv2
from googletrans import Translator

from utils import RED, GREEN, BLUE

# Needs to be moved into a utility function of it's own
os.environ["root"] = os.path.dirname(os.getcwd())

# Need to read into: https://tesseract-ocr.github.io/tessdoc/ImproveQuality
# Lots of image pre-processing is required T_T
def enhance(image_path):
    print(RED + f'Pre-process image... \n')
    img = cv2.imread(image_path)

    # Resize img, with manually specified the output size 
    #  scaling factor for the width and height of the image
    # bicubic interpolation method, produces smoother and higher-quality results 
        # interpolation when resizing
    img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    

    # apply dilation and erosion
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    img = cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    return img

# Function will pre-process image, then try to detect text and draw rectangles around it
def annotate_textbox(image):
    print(RED + f'Annotating image... \n')

    # Initialize variables for the largest rectangle
    max_area = 0
    max_rect = None

    d = pytesseract.image_to_data(image, output_type=Output.DICT)
    n_boxes = len(d['level'])
    for i in range(n_boxes):
        (text,x,y,w,h) = (d['text'][i],d['left'][i],d['top'][i],d['width'][i],d['height'][i])
        cv2.rectangle(image, (x,y), (x+w,y+h) , (0,255,0), 2)

def extract_text(image):
    text = pytesseract.image_to_string(image)
    print(BLUE + text)
    return text

def translate_text(image, text):
    print(BLUE + 'Translating text...')
    # Create an instance of the Translator
    translator = Translator()

    # Specify the text and the target language for translation
    target_language = "es"  # Language code for Spanish
    if (text != None):
        translation = translator.translate(text, dest=target_language)
    print(BLUE + translation.text)
    return translation.text

# Utility function to verify file is an image
# Returns a boolean value!
def is_image_file(file_path):
    # Image extensions to support
    image_extensions = ['.jpg', '.png', '.jpeg', '.gif', '.bmp']
    # Split into base/extension tuple and then provide the extension in tuple
    extension = os.path.splitext(file_path)[1]
    return extension.lower() in image_extensions

def main():
    print("Importing images from text sample directory....")

    # Example usage
    folder_path = os.environ.get("root")+'/data'
    pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

    # Function iterates through all images in a given folder
    # Get a list of all files in the folder
    image_list = os.listdir(folder_path)
    # Clean up counter var later
    img_count = 0

    # Iterate over each file in the folder
    for image_file in image_list:
        if is_image_file(image_file):
            img_count += 1
            print(GREEN + f'Import image {img_count}/{len(image_list)}')

            file_path = os.path.join(folder_path, image_file)

            # Open the image file
            image = enhance(file_path)
            
            text = extract_text(image)
            new_text = translate_text(enhance(file_path), text)

            annotate_textbox(image)
            
            # Display the image with the text block border
            cv2.imshow("Text Block", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__ == "__main__":
    main()