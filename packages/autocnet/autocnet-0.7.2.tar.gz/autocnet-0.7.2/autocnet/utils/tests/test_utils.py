import unittest
import numpy as np
import pandas as pd

from osgeo import ogr
from .. import utils


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_cross_form(self):
        a = np.array([-1, 0, 1.25])
        np.testing.assert_array_almost_equal(utils.crossform(a), np.array([[0., -1.25,  0.],
                                                                           [1.25,  0.,  1.],
                                                                           [-0., -1.,  0.]]))

    def test_checkbandnumbers(self):
        self.assertTrue(utils.checkbandnumbers([1,2,3,4,5], (2,5,1)))
        self.assertFalse(utils.checkbandnumbers([1,2,4], (1,2,3)))
        self.assertTrue(utils.checkbandnumbers([1.0, 2.0, 3.0], [1.0]))
        self.assertFalse(utils.checkbandnumbers([-1.0, 2.0, 3.0], (1.0, 2.0, 3.0)))

    def test_getdeplaid(self):
        self.assertEqual(utils.checkdeplaid(95), 'night')
        self.assertEqual(utils.checkdeplaid(127.4), 'night')
        self.assertEqual(utils.checkdeplaid(180), 'night')
        self.assertEqual(utils.checkdeplaid(94.99), 'night')
        self.assertEqual(utils.checkdeplaid(90), 'night')
        self.assertEqual(utils.checkdeplaid(26.1), 'day')
        self.assertEqual(utils.checkdeplaid(84.99), 'day')
        self.assertEqual(utils.checkdeplaid(0), 'day')
        self.assertFalse(utils.checkdeplaid(-1.0))

    def test_checkmonotonic(self):
        self.assertTrue(utils.checkmonotonic(np.arange(10)))
        self.assertTrue(utils.checkmonotonic(range(10)))
        self.assertFalse(utils.checkmonotonic([1,2,4,3]))
        self.assertFalse(utils.checkmonotonic([-2.0, 0.0, -3.0]))

        self.assertEqual(utils.checkmonotonic(np.arange(10), piecewise=True),
                [True] * 10)
        self.assertEqual(utils.checkmonotonic(range(10), piecewise=True),
                [True] * 10)
        self.assertEqual(utils.checkmonotonic([1,2,4,3], piecewise=True),
                [True,True,True, False])
        self.assertEqual(utils.checkmonotonic([-2.0, 0.0, -3.0],piecewise=True),
                [True,True,False])

    def test_getnearest(self):
        iterable = range(10)
        idx, value = utils.getnearest(iterable, 3)
        self.assertEqual(idx, 3)

        idx, value = utils.getnearest(iterable, 8.32)
        self.assertEqual(idx, 8)

        idx, value = utils.getnearest(iterable, 8.5)
        self.assertEqual(idx, 8)

        idx, value = utils.getnearest(iterable, 8.51)
        self.assertEqual(idx, 9)

    def test_find_in_dict(self):
        d = {'a':1,
            'b':2,
            'c':{
                'd':3,
                'e':4,
                'f':{
                    'g':5,
                    'h':6
                    }
                }
            }

        self.assertEqual(utils.find_in_dict(d, 'a'), 1)
        self.assertEqual(utils.find_in_dict(d, 'f'), {'g':5,'h':6})
        self.assertEqual(utils.find_in_dict(d, 'e'), 4)

    def test_find_nested_in_dict(self):
        d = {'a':1,
            'b':2,
            'c':{
                'd':3,
                'e':4,
                'f':{
                    'g':5,
                    'h':6
                    }
                }
            }

        self.assertEqual(utils.find_nested_in_dict(d, 'a'), 1)
        self.assertEqual(utils.find_nested_in_dict(d, ['c', 'f', 'g']), 5)

    def test_make_homogeneous(self):
        pts = np.arange(50).reshape(25,2)
        pts = utils.make_homogeneous(pts)
        self.assertEqual(pts.shape, (25,3))
        np.testing.assert_array_equal(pts[:, -1], np.ones(25))

    def test_remove_field_name(self):
        starray = np.array([(1 ,2.,'String'), (2, 3.,"String2")],
              dtype=[('index', 'i4'),('bar', 'f4'), ('baz', 'S10')])
        truth = np.array([(2.,'String'), (3.,"String2")],
              dtype=[('bar', 'f4'), ('baz', 'S10')])
        cleaned_array = utils.remove_field_name(starray, 'index')
        np.testing.assert_array_equal(cleaned_array, truth)

    def test_slope(self):
        x1 = pd.DataFrame({'x': np.arange(1, 11),
                           'y': np.arange(1, 11)})
        x2 = pd.DataFrame({'x': np.arange(6, 16),
                           'y': np.arange(11, 21)})

        slope = utils.calculate_slope(x1, x2)
        self.assertEqual(slope[0], 2)

    def test_array_to_poly(self):
        array1 = np.array([[1, 2],
                           [3, 4],
                           [5, 6]])
        array2 = np.array([[1, 2, 3],
                           [4, 5, 6],
                           [7, 8, 9]])
        geom1 = utils.array_to_poly(array1)

        self.assertIsInstance(geom1, ogr.Geometry)
        self.assertRaises(ValueError, utils.array_to_poly, array2)

    def test_dispatch(self):
        class Patchwork(object):

            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)

            @utils.methodispatch
            def get(self, arg):
                return getattr(self, arg, None)

            @get.register(list)
            def _(self, arg):
                return [self.get(x) for x in arg]

        patchwork = Patchwork(a=1, b=2, c=3)
        self.assertEqual(patchwork.get(['a', 'b']), [1, 2])
        self.assertEqual(patchwork.get('c'), 3)

    def test_decorate_class(self):
        class Test(object):
            def __init__(self):
                self.test = 'original'

            def get_test(self):
                return self.test

        def dec(func):
            return lambda x:'decorated'

        Dec_Test = utils.decorate_class(Test, dec)

        undecorated = Test()
        decorated = Dec_Test()

        self.assertEqual(undecorated.get_test(), 'original')
        self.assertEqual(decorated.get_test(), 'decorated')

        with self.assertRaises(Exception):
            utils.decorate_class(Test, 'Totally not a callable')

    def test_generate_decorator(self):
        def func_to_wrap(x):
            return x+1

        def wrapper():
            # Should be able to access run-time namespace
            return ret + 1, test

        decorator = utils.create_decorator(wrapper, test=0)
        wrapped_func = decorator(func_to_wrap)

        self.assertTrue(wrapped_func(1),2)
