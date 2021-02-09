import numpy as np
import matplotlib.pyplot as plt
import cv2

from helpers.shapes import rounded_rectangle
from helpers.resize import ResizeWithAspectRatio

image_document_w = 800
image_document_h = 600

image_document_margin = 40

target_w = image_document_w - image_document_margin
target_h = image_document_h - image_document_margin

corner_radius = 0.1

# ///////////////////////////////////////////////////////////////////////
# Dimensions in millimetres for TD3/MRP

doc_w = 125
doc_h = 88

mrz_h = 17
mrz_w = 118

mrz_h_margin_top = 3.2
mrz_h_margin_bot = 3

mrz_w_margin_lef = 3
mrz_w_margin_rig = 3  # probably

# ///////////////////////////////////////////////////////////////////////

img = np.zeros((doc_h, doc_w))
img = ResizeWithAspectRatio(img, target_w, target_h)
print(target_h, target_w)
print(img.shape)
img_h, img_w = img.shape
mm_to_px = img_w/doc_w

top_left_document_start   = (0,0)
bottom_right_document_end = (round(img_h), round(img_w))

color = (255, 255, 255, 1)
image_size = (round(img_h), round(img_w), 4)
img = np.zeros(image_size)
img = rounded_rectangle(img, top_left_document_start, bottom_right_document_end, color=color, radius=corner_radius, thickness=-1)

plt.imshow(img)
plt.show()



