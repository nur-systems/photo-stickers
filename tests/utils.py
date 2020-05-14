import numpy as np
from PIL import Image


def image_from_lists(pixel_list):
    pixel_array = np.uint8(pixel_list)
    image = Image.fromarray(pixel_array)
    return pixel_array, image
