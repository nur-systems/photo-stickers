import numpy as np
from PIL import Image
import cv2


def as_numpy_rgba(image):
    image_rgba = image.convert('RGBA')
    return np.asarray(image_rgba)


def get_mask_data(image, mask):
    as_sized = mask.resize(image.size, Image.ANTIALIAS)
    as_numpy = as_numpy_rgba(as_sized)
    return as_numpy[:, :, 0]


def combine_mask(image_channels, mask_channel):
    mask_data_channel = mask_channel.reshape(*mask_channel.shape, 1)
    image_data = np.concatenate([image_channels[:, :, :3], mask_data_channel], axis=-1)
    return Image.fromarray(image_data)


def segment(image, mask):
    image_data = as_numpy_rgba(image)
    mask_data = get_mask_data(image, mask)
    image_masked = combine_mask(image_data, mask_data)
    return image_masked


def crop_bbox(masked_image):
    mask_data = np.asarray(masked_image)
    x, y, w, h = cv2.boundingRect(mask_data[:, :, 3])
    cropped_data = mask_data[y:(y + h), x:(x + w), :]
    return Image.fromarray(cropped_data)
