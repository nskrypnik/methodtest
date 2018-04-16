
from tests import pytest, unittest
from methodtest.array_flattener import flatten_array, ParameterError


class ArrayFlattenerTest(unittest.TestCase):

    def test_flatten_array(self):
        """
        Test a number of use cases
        """
        self.assertEqual(flatten_array([1, 2, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(flatten_array([[1,2,[3]],4]), [1, 2, 3, 4])
        self.assertEqual(flatten_array([1, 3, [[5]], [[[6]]], 7, [[8]]]), [1, 3, 5, 6, 7, 8])
        self.assertEqual(flatten_array([[[[[[6]]]]]]), [6])
        self.assertEqual(flatten_array([[[[[[1], 2], 3, 4], 5], 6], 7]), [1, 2, 3, 4, 5, 6, 7])

    def test_empty_array(self):
        """
        Test case when input is empty array
        """
        self.assertEqual(flatten_array([]), [])

    def test_single_int(self):
        """
        Test when input is a single integer
        """
        self.assertEqual(flatten_array(1), [1])
        self.assertEqual(flatten_array(7), [7])

    def test_element_is_not_integer(self):
        with pytest.raises(ParameterError) as e:
            flatten_array('e')
        with pytest.raises(ParameterError) as e:
            flatten_array([1, 2, [6, 'o']])
