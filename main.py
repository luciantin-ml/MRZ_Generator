import cv2
import matplotlib.pyplot as plt
import json
import numpy as np
from PIL import ImageFont, ImageDraw, Image

from helpers.data_gen import create_person
from helpers.document import create_document, create_blank_test
import random


with open('settings.json', 'r') as settings_file:
    data = settings_file.read()
    settings = json.loads(data)

image_document_w = settings['image_w']
image_document_h = settings['image_h']

image_document_margin = 40

target_w = image_document_w - image_document_margin
target_h = image_document_h - image_document_margin


MRZ_code, MRZ_data = create_person()

img, mask = create_document(target_w, target_h, MRZ_code, MRZ_data, settings)

plt.imshow(img)
plt.show()
plt.imshow(mask)
plt.show()
plt.imshow(create_blank_test())
plt.show()











