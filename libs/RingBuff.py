"""
Ring Buffer classes implemented by traditional python data structs(lists and deques) and numpy based arrays
"""

import numpy as np
from collections import deque
import itertools


class RingBuffBase(object):
    def __init__(self, size_max):
        self.cap = size_max  # capacity of buffer
        self.head = 0  # offset to oldest entry
        self.tail = 0  # offset to newest entry
        self.size = 0  # current number of entries in buffer
        self._buffer = None  # buffer itself

    def write(self, val):
        pass

    def write_vals(self, vals):
        pass

    def append(self, val):
        self.cap += 1

    def append_vals(self, vals):
        self.cap += len(vals)

    def get_all(self):
        """return a list of elements from the oldest to the newest"""
        return self._buffer

    def get_partial(self):
        """return a partial list of elements from oldest to newest"""
        pass

    def __getitem__(self, key):
        """get element"""
        return self._buffer[key]

    def __repr__(self):
        """return string representation"""
        pass


class RingBuff_Deque(RingBuffBase):
    """
    Deque based ring buffer
    """
    def __init__(self, *args, **kwargs):
        super(RingBuff_Deque, self).__init__(*args, **kwargs)
        self._buffer = deque(self.cap)


class RingBuff_List(RingBuffBase):
    """
    list based ring buffer
    """
    def __init__(self, *args, **kwargs):
        super(RingBuff_List, self).__init__(*args, **kwargs)
        self._buffer = [None * self.cap]


class RingBuff_NP(RingBuffBase):
    """
    Numpy based ring buffer
    """
    def __init__(self, _dtype=np.float64, *args, **kwargs):
        super(RingBuff_NP, self).__init__(*args, **kwargs)
        self._data = np.zeros(self.cap, dtype=_dtype)


# class RingBuffer(object):
#     def __init__(self, size_max, _dtype=np.float64):
#         """initialization"""
#         self.size_max = size_max
#         self._data = np.zeros(size_max, dtype=_dtype)
#         # self._data.fill(default_value)
#         self.size = 0
#
#     def append(self, value):
#         """append an element"""
#         self._data = np.roll(self._data, 1)
#         self._data[0] = value
#         self.size += 1
#         if self.size == self.size_max:
#             self.__class__  = RingBufferFull
#
#     def get_all(self):
#         """return a list of elements from the oldest to the newest"""
#         return self._data
#
#     def get_partial(self):
#         """return a partial list of elements from oldest to newest"""
#         return self.get_all()[0:self.size]
#
#     def __getitem__(self, key):
#         """get element"""
#         return self._data[key]
#
#     def __repr__(self):
#         """return string representation"""
#         s = self._data.__repr__()
#         s = s + '\t' + str(self.size)
#         s = s + '\t' + self.get_all()[::-1].__repr__()
#         s = s + '\t' + self.get_partial()[::-1].__repr__()
#         return s
#
#
# class RingBufferFull(RingBuffer):
#     def append(self, value):
#         """append an element when buffer is full"""
#         self._data = np.roll(self._data, 1)
#         self._data[0] = value
