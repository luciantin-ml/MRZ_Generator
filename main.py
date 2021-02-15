import cv2
import matplotlib.pyplot as plt
import json
import os
from helpers.data_gen import create_person
from helpers.document import create_document, create_blank_test
from imantics import Mask, Image, Category, Dataset
from helpers.transform import random_transform

with open('settings.json', 'r') as settings_file:
    data = settings_file.read()
    settings = json.loads(data)

image_document_w = settings['image_w']
image_document_h = settings['image_h']

image_document_margin = 40

target_w = image_document_w - image_document_margin
target_h = image_document_h - image_document_margin

# MRZ_code, MRZ_data = create_person()
# img, mask, MRZ_BB = create_document(target_w, target_h, MRZ_code, MRZ_data)
#
# print(MRZ_data)
#
# plt.imshow(img)
# plt.show()
# plt.imshow(mask, cmap='gray')
# plt.show()
# plt.imshow(create_blank_test())
# plt.show()

cwd = os.getcwd()
res_pth = os.path.join(cwd,'result')
image_res_pth = os.path.join(res_pth,'images')
mask_res_pth = os.path.join(res_pth,'masks')
# rel_res_pth = os.path.join('./')

dataset = Dataset('pass')
mask_category = Category("MRZ")

for id in range(settings['sample_size']):
    MRZ_code, MRZ_data = create_person()
    img, mask, MRZ_BB = create_document(target_w, target_h, MRZ_code, MRZ_data)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)

    img, mask = random_transform(img, mask)

    cv2.imwrite(os.path.join(image_res_pth, str(id)+'.png'),  cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    cv2.imwrite(os.path.join(mask_res_pth, str(id)+'.bmp'), mask)

    # image = Image.from_path('./result/images/'+str(id)+'.png')
    # mask = Mask(mask)
    # image.add(mask, category=mask_category)
    # image.add(mask, category=Category("MRRZ")) #
    # dataset.add(image)

    # dict of coco #
    # coco_json = image.export(style='coco') #
    # Saves to file #
    # image.save('result/annotation.json', style='coco') #

    print(id)


# with open('result/annotation.json', 'w') as fp:
#     json.dump(dataset.export(style='coco'), fp)







