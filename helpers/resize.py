import cv2


def ResizeWithAspectRatio(img, target_w, target_h):
    doc_h, doc_w = img.shape
    print(doc_h,doc_w)
    img_h = 0
    img_w = 0

    if (doc_w / doc_h) > (target_w / target_h):
        ratio = target_w / doc_w
        img_h = doc_h * ratio
        img_w = target_w
    else:
        ratio = target_h / doc_h
        img_w = doc_w * ratio
        img_h = target_h

    img = cv2.resize(img, (round(img_w), round(img_h)))
    return img


def Resize(img, target_w, target_h):
    return 'ds'
