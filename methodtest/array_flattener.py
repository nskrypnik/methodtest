"""
The module provides function to flatten any given nested array of integer
numbers.
"""

class ParameterError(Exception):
    pass

def flatten_array(array):
    """Flaten nested array of integer numbers. Example
            flatten_array([[1,2,[3]],4]) -> [1, 2, 3, 4]
        Args:
            array: A nested/flat array of integer numbers or just an integer number
        Returns:
            Flattened array of integer numbers
        Raises:
            ParameterError: When one of elements of array is not an integer
    """
    if type(array) == list:
        flatten = []
        for item in array:
            flatten += flatten_array(item)
        return flatten
    elif type(array) == int:
        # if given parameter is just a number - return that
        # number as a single item list
        return [array]
    else:
        raise ParameterError('Wrong input type, should be integer or an array of integers')
