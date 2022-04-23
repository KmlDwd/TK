import cv2
import numpy as np
import requests


def load_path_url_images(template_img, local_path_img):
    if template_img[0:4] == "http":
        try:
            resp = requests.get(template_img, stream=True).raw
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        except:
            return "Error: Unable to load template image from url!"

    else:
        image = cv2.imread(template_img)

    shape = image.shape[:2]
    image2 = cv2.imread(local_path_img)

    try:
        image2 = cv2.resize(image2, shape)
    except:
        return "Error: Unable to load template image from path!"

    return find_by_knn(image, image2)


def find_by_knn(img, img2):
    #  The shorter the distance, the more similar the images will be.
    img, img2 = np.reshape(np.array(img), (1, -1)), np.reshape(np.array(img2), (1, -1))
    dists = list(np.sqrt(np.sum((img2 - img) ** 2, axis=1)))
    return dists[0]
