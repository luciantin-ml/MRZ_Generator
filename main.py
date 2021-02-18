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

image_document_w = 800
image_document_h = 600

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

dataset_MRZ_result = {}

dataset = Dataset('pass')
mask_category = Category("MRZ")
# settings['sample_size']
for id in range(settings['sample_size']):
    print(id)
    # grozan nacin za error handling ali ponekad generira krivi datum i ponekad se dobije slika krive velicine,
    # nisam skuzio zasto, i onda ne radi dodavanje dokumenta na background, rijetko
    ok = False
    while not ok:
        try:
            MRZ_code, MRZ_data = create_person()
            img, mask, MRZ_BB = create_document(target_w, target_h, MRZ_code, MRZ_data)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
            img, mask = random_transform(img, mask)
            cv2.imwrite(os.path.join(image_res_pth, str(id) + '.png'), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            cv2.imwrite(os.path.join(mask_res_pth, str(id) + '.bmp'), mask)
            dataset_MRZ_result[id] = {}
            dataset_MRZ_result[id]['code'] = MRZ_code
            dataset_MRZ_result[id]['data'] = MRZ_data
        except:
            ok = False
        else:
            ok = True

with open(os.path.join(res_pth, 'MRZ_values.json'), 'a') as mrz_vals:
    json.dump(dataset_MRZ_result, mrz_vals)

print('TJT')

# with open('result/annotation.json', 'w') as fp:
#     json.dump(dataset.export(style='coco'), fp)


# print(ok)
# MRZ_code, MRZ_data = create_person()
# img, mask, MRZ_BB = create_document(target_w, target_h, MRZ_code, MRZ_data)
# img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
# img, mask = random_transform(img, mask)
# cv2.imwrite(os.path.join(image_res_pth, str(id) + '.png'), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
# cv2.imwrite(os.path.join(mask_res_pth, str(id) + '.bmp'), mask)






