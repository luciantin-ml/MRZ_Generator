import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from numpy.lib import recfunctions as rfn
from helpers.resize import ResizeWithAspectRatio, Resize
from helpers.shapes import rounded_rectangle
import matplotlib.pyplot as plt
import glob
import cv2
import random
# ///////////////////////////////////////////////////////////////////////
# Dimensions in millimetres for TD3/MRP

corner_radius = 0.1

doc_w = 125
doc_h = 88

doc_margin = 3

mrz_h = 17
mrz_w = 118

mrz_h_margin_top = 3.2
mrz_h_margin_bot = 3

mrz_w_margin_lef = 3
mrz_w_margin_rig = 3  # probably

font_width = 2.54

heading_width = 8
image_start_y = heading_width + doc_margin*2
image_h = 65
image_w = 30



text_w = doc_w - image_w - doc_margin*3
text_h = image_h
text_row_start_x = image_w + doc_margin*2
text_row_start_y = image_start_y

text_cols = 2
text_rows = 4
margin_betw_text_rows = 2
margin_betw_text_cols = 4
text_row_h = (text_h/text_rows) - (margin_betw_text_rows * (text_rows-1))  # NE RADI KAKO TREBA ali ok
text_col_w = text_w/text_cols

# ///////////////////////////////////////////////////////////////////////

fontpath = './helpers/fonts/OcrB Regular.ttf'
font_code = ImageFont.truetype(fontpath, 27, layout_engine=ImageFont.LAYOUT_BASIC)
font_small = ImageFont.truetype(fontpath, 27, layout_engine=ImageFont.LAYOUT_BASIC)
font_normal = ImageFont.truetype(fontpath, 27, layout_engine=ImageFont.LAYOUT_BASIC)
font_large = ImageFont.truetype(fontpath, 27, layout_engine=ImageFont.LAYOUT_BASIC)

def create_blank_test():
    img = np.zeros((doc_h, doc_w, 3), np.uint8)
    img = cv2.rectangle(img, (doc_margin,doc_margin), (doc_w-doc_margin,doc_margin+8,), (255,255,255), -1) # heading
    img = cv2.rectangle(img, (doc_margin,image_start_y), (doc_margin+image_w, image_h), (255,255,255), -1) # image
    img = cv2.rectangle(img, (text_row_start_x, text_row_start_y), (text_row_start_x+text_w, text_h), (255,255,255), -1) # text

    for i in range(text_cols):
        top_l = ( round(text_row_start_x+text_col_w*i+margin_betw_text_cols*i),  round(text_row_start_y))
        bot_r = ( round(text_row_start_x+text_col_w*(i+1)),  round(text_h))
        img = cv2.rectangle(img, top_l, bot_r, (20*i, 0, 255), -1)  # text
        for j in range(text_rows):
            top_l = (
                round(text_row_start_x + text_col_w * i + margin_betw_text_cols * i),
                round(text_row_start_y + text_row_h * j + margin_betw_text_rows * (j+1))
            )
            bot_r = (
                round(text_row_start_x + text_col_w * (i + 1)),
                round(text_row_start_y + text_row_h * (j + 1) + margin_betw_text_rows * (j+1))
            )
            img = cv2.rectangle(img, top_l, bot_r, (255, 0, 255), -1)  # text

    x1 = mrz_w_margin_lef
    y1 = doc_h - mrz_h_margin_bot - mrz_h
    x2 = x1 + mrz_w
    y2 = doc_h - mrz_h_margin_bot

    top_left_MRZ_corner = (round(x1 ), round(y1 ))
    bot_right_MRZ_corner = (round(x2 ), round(y2 ))

    img = cv2.rectangle(img, top_left_MRZ_corner, bot_right_MRZ_corner, (0,255,0), -1)

    return img

def create_document_background(target_w, target_h):
    bckg = [cv2.imread(file) for file in glob.glob("helpers/images/document_background/*.bmp")]
    bckg = random.choice(bckg)
    bckg = cv2.cvtColor(bckg, cv2.COLOR_BGR2BGRA)

    img = np.zeros((doc_h, doc_w, 3), np.uint8)
    img = ResizeWithAspectRatio(img, target_w, target_h)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGRA)

    img_h, img_w, pixels = img.shape

    bckg = Resize(bckg, img_w, img_h)

    # print(img.shape,bckg.shape)

    top_left_document_start = (0, 0)
    bottom_right_document_end = (round(img_h), round(img_w))
    color = (255, 255, 255, 1)
    bckg = rounded_rectangle(bckg, top_left_document_start, bottom_right_document_end, color=color, radius=corner_radius,thickness= 1)

    img = cv2.addWeighted(img,1,bckg,1,0)

    return img





def create_document(target_w, target_h, MRZ_code, MRZ_data, settings):

    img = create_document_background(target_w, target_h)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_h, img_w, pixels = img.shape

    mask = np.zeros((img_h, img_w, 1), np.uint8)
    px_per_mm = img_w / doc_w

    # MRZ POS
    x1 = mrz_w_margin_lef
    y1 = doc_h - mrz_h_margin_bot - mrz_h
    x2 = x1 + mrz_w
    y2 = doc_h - mrz_h_margin_bot

    top_left_MRZ_corner = (round(x1 * px_per_mm), round(y1 * px_per_mm))
    bot_right_MRZ_corner = (round(x2 * px_per_mm), round(y2 * px_per_mm))

    #  MARK MRZ RECTANGLE
    # mask = cv2.rectangle(mask, top_left_MRZ_corner, bot_right_MRZ_corner, (1), -1)
    # img = cv2.rectangle(img, top_left_MRZ_corner, bot_right_MRZ_corner, (0,0,0), 2)

    MRZ_code = MRZ_code.split('\n', 2)
    first_MRZ_line = MRZ_code[0]
    second_MRZ_line = MRZ_code[1]

    b, g, r, a = 0, 0, 0, 0
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)

    draw.text((round(3.6 * px_per_mm), round(y1 * px_per_mm) + 15), first_MRZ_line, font=font_code, fill=(b, g, r, a))
    draw.text((round(3.6 * px_per_mm), round(y1 * px_per_mm) + 55 + 3), second_MRZ_line, font=font_code, fill=(b, g, r, a))

    #   MRZ TEXT POS

    img = np.array(img)
    font_w, font_h = font_code.getsize(first_MRZ_line)

    #  ZA TESTIRANJE
    # mask = cv2.rectangle(mask, (round(3.6 * px_per_mm), round(y1 * px_per_mm) + 15), (round(3.6 * px_per_mm)+font_w, round(y1 * px_per_mm) + 15+font_h), (1), -1)
    # img = cv2.rectangle(img, (round(3.6 * px_per_mm), round(y1 * px_per_mm) + 15), (round(3.6 * px_per_mm)+font_w, round(y1 * px_per_mm) + 15+font_h),(0,0,0), 2)
    # img = cv2.rectangle(img, (round(3.6 * px_per_mm), round(y1 * px_per_mm) + 55 + 3), (round(3.6 * px_per_mm)+font_w, round(y1 * px_per_mm) + 55 + 3 +font_h),(0,0,0), 2)

    mask = cv2.rectangle(mask, (round(3.6 * px_per_mm), round(y1 * px_per_mm) + 15), (round(3.6 * px_per_mm)+font_w, round(y1 * px_per_mm) + 15+font_h), (1), -1)
    mask = cv2.rectangle(mask, (round(3.6 * px_per_mm), round(y1 * px_per_mm) + 55 + 3), (round(3.6 * px_per_mm)+font_w, round(y1 * px_per_mm) + 55 + 3 +font_h), (1), -1)


    return img, mask



