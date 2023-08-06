import math
import os
import sys
import unittest
from unittest.mock import patch, Mock
import logging


from skimage import transform as tf
from skimage.util import img_as_float   
from skimage import color 
from skimage import data

import pytest

import numpy as np
from imageio import imread

from plio.io.io_gdal import GeoDataset

from autocnet.examples import get_path
import autocnet.matcher.subpixel as sp
from autocnet.transformation import roi

@pytest.fixture
def iris_pair(): 
    angle = 200
    scale = 1.4
    shiftr = 30
    shiftc = 10

    image = color.rgb2gray(data.retina())
    translated = image[shiftr:, shiftc:]
    rotated = tf.rotate(translated, angle)
    rescaled = tf.rescale(rotated, scale)
    sizer, sizec = image.shape
    rts_image = rescaled[:sizer, :sizec] 
    return image, rts_image

@pytest.fixture
def apollo_subsets():
    # These need to be geodata sets or just use mocks...
    arr1 = imread(get_path('AS15-M-0295_SML(1).png'))[100:201, 123:224]
    arr2 = imread(get_path('AS15-M-0295_SML(2).png'))[235:336, 95:196]
    return arr1, arr2


@pytest.mark.parametrize("center_x, center_y, size, expected", [(4, 4, 9, 404),
                                                          (55.4, 63.1, 27, 6355)])
def test_clip_roi(center_x, center_y, size, expected):
    img = np.arange(10000).reshape(100, 100)

    clip, axr, ayr = sp.clip_roi(img, center_x, center_y, size)

    assert clip.mean() == expected

def clip_side_effect(*args, **kwargs):
    if np.array_equal(a, args[0]):
        return a, 0, 0
    else:
        center_y = b.shape[0] / 2
        center_x = b.shape[1] / 2
        bxr, bx = math.modf(center_x)
        byr, by = math.modf(center_y)
        bx = int(bx)
        by = int(by)
        return b[by-10:by+11, bx-10:bx+11], bxr, byr

def test_subpixel_template(apollo_subsets):
    a = apollo_subsets[0]
    b = apollo_subsets[1]
    with patch('autocnet.matcher.subpixel.clip_roi', side_effect=clip_side_effect):
        nx, ny, strength, _ = sp.subpixel_template(a.shape[1]/2, a.shape[0]/2,
                                                b.shape[1]/2, b.shape[0]/2,
                                                a, b, upsampling=16)

    assert strength >= 0.99
    assert nx == 50.5
    assert ny == 52.4375

@pytest.mark.parametrize("loc, failure", [((0,4), True),
                                          ((4,0), True),
                                          ((1,1), False)])
def test_subpixel_template_at_edge(apollo_subsets, loc, failure):
    a = apollo_subsets[0]
    b = apollo_subsets[1]

    def func(*args, **kwargs):
        corr = np.zeros((10,10))
        corr[loc[0], loc[1]] = 10
        return 0, 0, 0, corr

    with patch('autocnet.matcher.subpixel.clip_roi', side_effect=clip_side_effect):
        if failure:
            # with pytest.warns(UserWarning, match=r'Maximum correlation \S+'):
            # match=r'Maximum correlation \S+'
            nx, ny, strength, _ = sp.subpixel_template(a.shape[1]/2, a.shape[0]/2,
                                                    b.shape[1]/2, b.shape[0]/2,
                                                    a, b, upsampling=16,
                                                    func=func)
        else:
            nx, ny, strength, _ = sp.subpixel_template(a.shape[1]/2, a.shape[0]/2,
                                                        b.shape[1]/2, b.shape[0]/2,
                                                        a, b, upsampling=16,
                                                        func=func)
            assert nx == 50.5

def test_subpixel_transformed_template(apollo_subsets):
    a = apollo_subsets[0]
    b = apollo_subsets[1]
    transform = tf.AffineTransform(rotation=math.radians(1), scale=(1.1,1.1))
    with patch('autocnet.matcher.subpixel.clip_roi', side_effect=clip_side_effect):
        nx, ny, strength, _ = sp.subpixel_transformed_template(a.shape[1]/2, a.shape[0]/2,
                                                b.shape[1]/2, b.shape[0]/2,
                                                a, b, transform, upsampling=16)

    assert strength >= 0.83
    assert nx == pytest.approx(50.576284)
    assert ny == pytest.approx(54.0081)


def test_estimate_logpolar_transform(iris_pair):
    img1, img2 = iris_pair 
    affine = sp.estimate_logpolar_transform(img1, img2) 

    assert pytest.approx(affine.scale, 0.1) == 0.71
    assert pytest.approx(affine.rotation, 0.1) == 0.34 
    assert pytest.approx(affine.translation[0], 0.1) == 283.68
    assert pytest.approx(affine.translation[1], 0.1) == -198.62 


def test_fourier_mellen(iris_pair):
    img1, img2 = iris_pair 
    nx, ny, error = sp.fourier_mellen(img1, img2, phase_kwargs = {"reduction" : 11, "size":(401, 401), "convergence_threshold" : 1, "max_dist":100}) 
    
    assert pytest.approx(nx, 0.01) == 996.39 
    assert pytest.approx(ny, 0.01) ==  984.912 
    assert pytest.approx(error, 0.01) == 0.0422 


@pytest.mark.parametrize("loc, failure", [((0,4), True),
                                          ((4,0), True),
                                          ((1,1), False)])
def test_subpixel_transformed_template_at_edge(apollo_subsets, loc, failure):
    a = apollo_subsets[0]
    b = apollo_subsets[1]

    def func(*args, **kwargs):
        corr = np.zeros((5,5))
        corr[loc[0], loc[1]] = 10
        return 0, 0, 0, corr

    transform = tf.AffineTransform(rotation=math.radians(1), scale=(1.1,1.1))
    with patch('autocnet.matcher.subpixel.clip_roi', side_effect=clip_side_effect):
        if failure:
            print(a.shape[1]/2, a.shape[0]/2,b.shape[1]/2, b.shape[0]/2,
                                                    a, b)
            nx, ny, strength, _ = sp.subpixel_transformed_template(a.shape[1]/2, a.shape[0]/2,
                                                    b.shape[1]/2, b.shape[0]/2,
                                                    a, b, transform, upsampling=16,
                                                    func=func)
        else:
            nx, ny, strength, _ = sp.subpixel_transformed_template(a.shape[1]/2, a.shape[0]/2,
                                                        b.shape[1]/2, b.shape[0]/2,
                                                        a, b, transform, upsampling=16,
                                                        func=func)
            assert nx == 50.5

@pytest.mark.parametrize("convergence_threshold, expected", [(2.0, (50.49, 52.08, -9.5e-20))])
def test_iterative_phase(apollo_subsets, convergence_threshold, expected):
    a = apollo_subsets[0]
    b = apollo_subsets[1]
    dx, dy, strength = sp.iterative_phase(a.shape[1]/2, a.shape[0]/2,
                                          b.shape[1]/2, b.shape[1]/2,
                                          a, b, 
                                          size=(51,51), 
                                          convergence_threshold=convergence_threshold,
                                          upsample_factor=100)
    assert dx == expected[0]
    assert dy == expected[1]
    if expected[2] is not None:
        # for i in range(len(strength)):
        assert pytest.approx(strength,6) == expected[2]

@pytest.mark.parametrize("data, expected", [
    ((21,21), (10, 10)),
    ((20,20), (10,10))
])
def test_check_image_size(data, expected):
    assert sp.check_image_size(data) == expected

@pytest.mark.parametrize("x, y, x1, y1, image_size, template_size, expected",[
    (4, 3, 4, 2, (5,5), (3,3), (4,2)),
    (4, 3, 4, 2, (7,7), (3,3), (4,2)),  # Increase the search image size
    (4, 3, 4, 2, (7,7), (5,5), (4,2)), # Increase the template size
    (4, 3, 3, 2, (7,7), (3,3), (4,2)), # Move point in the x-axis
    (4, 3, 5, 3, (7,7), (3,3), (4,2)), # Move point in the other x-direction
    (4, 3, 4, 1, (7,7), (3,3), (4,2)), # Move point negative in the y-axis
    (4, 3, 4, 3, (7,7), (3,3), (4,2))  # Move point positive in the y-axis

])
def test_subpixel_template_cooked(x, y, x1, y1, image_size, template_size, expected):
    test_image = np.array(((0, 0, 0, 0, 0, 0, 0, 1, 0),
                           (0, 0, 0, 0, 0, 0, 0, 1, 0),
                           (0, 0, 0, 1, 1, 1, 0, 1, 0),
                           (0, 0, 0, 0, 1, 0, 0, 0, 0),
                           (0, 0, 0, 0, 1, 0, 0, 0, 0),
                           (0, 0, 0, 0, 0, 0, 0, 0, 0),
                           (0, 0, 0, 0, 0, 0, 0, 0, 0),
                           (0, 0, 0, 0, 0, 0, 0, 0, 0),
                           (0, 0, 0, 0, 0, 0, 1, 1, 1),
                           (0, 1, 1, 1, 0, 0, 1, 0, 1),
                           (0, 1, 0, 1, 0, 0, 1, 0, 1),
                           (0, 1, 1, 1, 0, 0, 1, 0, 1),
                           (0, 0, 0, 0, 0, 0, 1, 1, 1)), dtype=np.uint8)

    # Should yield (-3, 3) offset from image center
    t_shape = np.array(((0, 0, 0, 0, 0, 0, 0, 0, 0),
                        (0, 0, 0, 1, 1, 1, 0, 0, 0),
                        (0, 0, 0, 0, 1, 0, 0, 0, 0),
                        (0, 0, 0, 0, 1, 0, 0, 0, 0),
                        (0, 0, 0, 0, 0, 0, 0, 0, 0)), dtype=np.uint8)

    dx, dy, corr, corrmap = sp.subpixel_template(x, y, x1, y1, 
                                                 test_image, t_shape,
                                                 image_size=image_size, 
                                                 template_size=template_size, 
                                                 upsampling=1)
    assert corr >= 1.0  # geq because sometime returning weird float > 1 from OpenCV
    assert dx == expected[0]
    assert dy == expected[1]

@pytest.mark.parametrize("x, y, x1, y1, image_size, expected",[
    (4, 3, 3, 2, (3,3), (3,2)),
    (4, 3, 3, 2, (5,5), (3,2)),  # Increase the search image size
    (4, 3, 3, 2, (5,5), (3,2)), # Increase the template size
    (4, 3, 2, 2, (5,5), (3,2)), # Move point in the x-axis
    (4, 3, 4, 3, (5,5), (3,2)), # Move point in the other x-direction
    (4, 3, 3, 1, (5,5), (3,2)), # Move point negative in the y-axis; also tests size reduction
    (4, 3, 3, 3, (5,5), (3,2))  # Move point positive in the y-axis

])
def test_subpixel_phase_cooked(x, y, x1, y1, image_size, expected):
    test_image = np.array(((0, 0, 0, 0, 0, 0, 0, 1, 0),
                           (0, 0, 0, 0, 0, 0, 0, 1, 0),
                           (0, 0, 0, 1, 1, 1, 0, 1, 0),
                           (0, 0, 0, 0, 1, 0, 0, 0, 0),
                           (0, 0, 0, 0, 1, 0, 0, 0, 0),
                           (0, 0, 0, 0, 0, 0, 0, 0, 0),
                           (0, 0, 0, 0, 0, 0, 0, 0, 0),
                           (0, 0, 0, 0, 0, 0, 0, 0, 0),
                           (0, 0, 0, 0, 0, 0, 1, 1, 1),
                           (0, 1, 1, 1, 0, 0, 1, 0, 1),
                           (0, 1, 0, 1, 0, 0, 1, 0, 1),
                           (0, 1, 1, 1, 0, 0, 1, 0, 1),
                           (0, 0, 0, 0, 0, 0, 1, 1, 1)), dtype=np.uint8)

    # Should yield (-3, 3) offset from image center
    t_shape = np.array(((0, 0, 0, 0, 0, 0, 0),
                        (0, 0, 1, 1, 1, 0, 0),
                        (0, 0, 0, 1, 0, 0, 0),
                        (0, 0, 0, 1, 0, 0, 0),
                        (0, 0, 0, 0, 0, 0, 0),
                        (0, 0, 0, 0, 0, 0, 0)), dtype=np.uint8)

    dx, dy, metrics, _ = sp.subpixel_phase(x, y, x1, y1, 
                                                 test_image, t_shape,
                                                 image_size=image_size)

    assert dx == expected[0]
    assert dy == expected[1]


def test_mutual_information(): 
    d_template = np.array([[i for i in range(50, 100)] for j in range(50)])
    s_image = np.ones((100, 100))
    s_image[25:75, 25:75] = d_template
    
    template = Mock(spec=roi.Roi, clipped_array = d_template)
    image = Mock(spec=roi.Roi, clipped_array = s_image)

    affine, max_corr, corr_map = sp.mutual_information_match(image, template, bins=20)
    assert affine.params[0][2] == -0.5171186125717124
    assert affine.params[1][2] == -0.5
    assert max_corr == 2.9755967600033015
    assert corr_map.shape == (51, 51)
    assert np.min(corr_map) >= 0.0