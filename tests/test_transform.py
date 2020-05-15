import numpy as np

from .utils import image_from_lists
from pystickers import transform


def test_as_numpy_rgba__rgba():
    pixels = [[[255, 0, 0, 0], [0, 255, 0, 0]],
              [[0, 0, 255, 0], [0, 0, 0, 255]]]
    pixel_array, image = image_from_lists(pixels)
    output_array = transform.as_numpy_rgba(image)
    assert np.equal(pixel_array, output_array).sum() == 16

def test_as_numpy_rgba__rgb():
    pixels = [[[255, 0, 0], [0, 255, 0]],
              [[0, 0, 255], [0, 0, 0]]]
    pixel_array, image = image_from_lists(pixels)
    output_array = transform.as_numpy_rgba(image)
    assert np.equal(pixel_array, output_array[:, :, :3]).sum() == 12
    assert (output_array[:, :, 3] == 255).sum() == 4

def test_get_mask_data__equal_size():
    pixels = [[[255, 0, 0], [0, 255, 0]],
              [[0, 0, 255], [0, 0, 0]]]
    mask = [[[255, 255, 255], [0, 0, 0]],
            [[  0,   0,   0], [0, 0, 0]]]
    pixel_array, image = image_from_lists(pixels)
    mask_array, mask_map = image_from_lists(mask)
    scaled_mask = transform.get_mask_data(image, mask_map)
    assert scaled_mask.shape[:2] == pixel_array.shape[:2]

def test_get_mask_data__smaller_size():
    pixels = [[[255, 0, 0], [0, 255, 0]],
              [[0, 0, 255], [0, 0, 0]]]
    mask = [[[255, 255, 255]]]
    pixel_array, image = image_from_lists(pixels)
    mask_array, mask_map = image_from_lists(mask)
    scaled_mask = transform.get_mask_data(image, mask_map)
    assert scaled_mask.shape[:2] == pixel_array.shape[:2]

def test_get_mask_data__larger_size():
    pixels = [[[255, 0, 0], [0, 255, 0]],
              [[0, 0, 255], [0, 0, 0]]]
    mask = [[[255, 255, 255], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[  0,   0,   0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[  0,   0,   0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
            [[  0,   0,   0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]
    pixel_array, image = image_from_lists(pixels)
    mask_array, mask_map = image_from_lists(mask)
    scaled_mask = transform.get_mask_data(image, mask_map)
    assert scaled_mask.shape[:2] == pixel_array.shape[:2]

def test_combine_mask():
    pixels = [[[255, 0, 0], [0, 255, 0]],
              [[0, 0, 255], [0, 0, 0]]]
    mask = [[128, 255],
            [ 64,   0]]
    pixel_array, image = image_from_lists(pixels)
    image_channels = transform.as_numpy_rgba(image)
    mask_channel = np.uint8(mask)
    masked_image = transform.combine_mask(image_channels, mask_channel)
    assert masked_image.size == image.size
    assert masked_image.getpixel((0, 0))[3] == 128
    assert masked_image.getpixel((1, 0))[3] == 255
    assert masked_image.getpixel((0, 1))[3] == 64
    assert masked_image.getpixel((1, 1))[3] == 0

def test_segment():
    pixels = [[[255, 0, 0], [0, 255, 0]],
              [[0, 0, 255], [0, 0, 0]]]
    mask = [[[128, 128, 128], [255, 255, 255]],
            [[ 64,  64,  64], [  0,   0,   0]]]
    pixel_array, image = image_from_lists(pixels)
    mask_array, mask_map = image_from_lists(mask)
    masked_image = transform.segment(image, mask_map)
    assert masked_image.size == image.size
    assert masked_image.getpixel((0, 0))[3] == 128
    assert masked_image.getpixel((1, 0))[3] == 255
    assert masked_image.getpixel((0, 1))[3] == 64
    assert masked_image.getpixel((1, 1))[3] == 0

