import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import glob
import random
from helpers.resize import ResizeWithAspectRatio, Resize

DOCUMENT_BACKGROUNDS = [cv2.imread(file) for file in glob.glob("helpers/images/background/*.bmp")]


def rotate_image(image, angle):
    return ndimage.rotate(image, angle, reshape=True)


def add_background_rgba(target_img, target_bckg, target_x, target_y, bckg_padding_x, bckg_padding_y):
    target_bckg = Resize(target_bckg, target_img.shape[0] + target_x + bckg_padding_x,
                         target_img.shape[1] + target_y + bckg_padding_y)
    # print(target_img.shape, bckg.shape)

    # y1, y2 = target_y, target_y + target_img.shape[0]
    y1, y2 = target_y, target_y + target_img.shape[0]
    # x1, x2 = target_x, target_y + target_img.shape[0]
    x1, x2 = target_x, target_x + target_img.shape[1]

    alpha_s = target_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    # print(target_img.shape, target_bckg.shape)

    for c in range(0, 3):
        t_i_a = alpha_s * target_img[:, :, c]
        # print(alpha_s.shape, alpha_l.shape, target_bckg[y1:y2, x1:x2, c].shape)
        t_b_a = alpha_l * target_bckg[y1:y2, x1:x2, c]
        target_bckg[y1:y2, x1:x2, c] = (t_i_a + t_b_a)

    return target_bckg


def random_transform(target_img, target_mask):
    root_angle_dir = random.choice([0, 1, 2])
    if root_angle_dir == 0:
        rot_angle = 30 + (round(random.random() * 30))
    elif root_angle_dir == 1:
        rot_angle = -30 - (round(random.random() * 30))
    else:
        rot_angle = 0
    # print(root_angle_dir)
    # rot_angle = 35
    # print(rot_angle)
    # print(target_img.shape, target_mask.shape)
    target_img = rotate_image(target_img, rot_angle)
    target_mask = rotate_image(target_mask, rot_angle)

    background = random.choice(DOCUMENT_BACKGROUNDS)
    # background = DOCUMENT_BACKGROUNDS[1]
    background = cv2.cvtColor(background, cv2.COLOR_BGR2RGBA)

    target_x = round(random.random() * 100)
    target_y = round(random.random() * 300)
    bckg_padding_x = round(random.random() * 100) + 200
    bckg_padding_y = round(random.random() * 100) + 200
    # target_img = add_background_rgba(target_img, background, target_x, target_y, bckg_padding_x, bckg_padding_y)
    target_img = add_background_rgba(target_img, background, target_x, target_y, bckg_padding_x, bckg_padding_y)

    b_shape = target_img.shape

    target_mask_h = b_shape[0]
    target_mask_w = b_shape[1]

    background_for_mask = np.zeros((target_mask_h, target_mask_w, 1), np.uint8)
    # mask_padding_top = 0
    # mask_padding_bot = 0
    # mask_padding_left = 0
    # mask_padding_right = 0
    # print(target_mask.shape, background_for_mask.shape)
    #  mask = cv2.copyMakeBorder(mask,
    #                           200,
    #                           200,
    #                           200,
    #                           200,
    #                           cv2.BORDER_CONSTANT, value=[0])
    # target_mask = cv2.bitwise_or(background_for_mask, target_mask)
    # target_mask =
    # print(background_for_mask.shape, target_mask.shape)

    y1, y2 = target_y, target_y + target_mask.shape[0]
    x1, x2 = target_x, target_x + target_mask.shape[1]
    background_for_mask[y1:y2, x1:x2] = target_mask

    return target_img, background_for_mask

# def skew_image(image, )
#
# img = cv2.imread('helpers/../result/images/1.png')
# mask = cv2.imread('helpers/../result/masks/1.bmp',-1)
#
# plt.imshow(mask)
# plt.show()
# # print(img.shape)
# plt.imshow(img)
# plt.show()
#
# # print(mask)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
#
# img, mask = random_transform(img, mask)
# print(img.shape, mask.shape)
#
# plt.imshow(mask)
# plt.show()
# # print(img.shape)
# plt.imshow(img)
# plt.show()


# img = rotate_image(img, 45)
# img2 = random.choice(DOCUMENT_BACKGROUNDS)
# img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGBA)
# bc = add_background_rgba(img, img2, 220, 100, 100, 100)
# plt.imshow(mask)
# plt.show()
# print(bc.shape)
# plt.imshow(bc)
# plt.show()
