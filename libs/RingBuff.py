"""
Ring Buffer classes implemented by traditional python data structs(lists and deques) and numpy based arrays
Based on Ring Buffer found on github
"""

import numpy as np
from collections import deque
import itertools


class RingBuffBase:
    """Skeleton Framework for a python implemented Ring Buffer"""
    def __init__(self, size_max):
        self.cap = size_max  # capacity of buffer
        self.size = 0  # current number of entries in buffer
        self._buffer = None  # buffer itself

    def write(self, val):
        pass

    def write_vals(self, vals):
        pass

    def get_all(self):
        """return a list of elements from the oldest to the newest"""
        pass

    def get_partial(self, N):
        """
        :param N: Number of entries to be fetched
        :return: entries in order of oldest to newest
        """
        pass

    def clear(self):
        del self._buffer
        self._buffer = None

    def __getitem__(self, key):
        """get element"""
        pass

    def __repr__(self):
        """return string representation"""
        return 'Ring Buffer Object of size {} with {} entries filled'.format(self.cap, self.size)


class RingBuff_Deque(RingBuffBase):
    """
    Deque based ring buffer
    """
    def __init__(self, *args, **kwargs):
        super(RingBuff_Deque, self).__init__(*args, **kwargs)
        self._buffer = deque(maxlen=self.cap)

    def __repr__(self):
        """return string representation"""
        return 'Deque based Ring Buffer Object of size {} with {} entries filled'.format(self.cap, self.size)


class RingBuff_List(RingBuffBase):
    """
    list based ring buffer
    """
    def __init__(self, *args, **kwargs):
        super(RingBuff_List, self).__init__(*args, **kwargs)
        self._buffer = [None] * self.cap

    def __repr__(self):
        """return string representation"""
        return 'List based Ring Buffer Object of size {} with {} entries filled'.format(self.cap, self.size)


class RingBuff_NP(RingBuffBase):
    """
    Numpy based ring buffer
    """
    def __init__(self, _dtype=np.float64, *args, **kwargs):
        super(RingBuff_NP, self).__init__(*args, **kwargs)
        self._buffer = np.zeros(self.cap, dtype=_dtype)
    
    def write(self, value):
        """append an element"""
        self._buffer = np.roll(self._buffer, 1)
        self._buffer[0] = value
        self.size += 1
        if self.size == self.cap:
            self.__class__ = RingBufferFull_NP

    def write_vals(self, vals):
        """appends a list of elements"""
        for entry in vals:
            self.write(entry)

    def get_all(self):
        """return a list of elements from the oldest to the newest"""
        return self._buffer

    def get_partial(self, n):
        """return a partial list of elements from oldest to newest"""
        return self.get_all()[0:n]

    def __getitem__(self, key):
        """"get element"""
        return self._buffer[key]

    def __repr__(self):
        """return string representation"""
        return 'NP based Ring Buffer Object of size {} with {} entries filled'.format(self.cap, self.size)


class RingBufferFull_NP(RingBuff_NP):
    def write(self, value):
        """append an element when buffer is full"""
        self._buffer = np.roll(self._buffer, 1)
        self._buffer[0] = value

    def write_vals(self, vals):
        """write a list of vals to buffer"""
        self._buffer = np.roll(self._buffer, len(vals))
        self._buffer[0:len(vals)] = vals

    def __repr__(self):
        """return string representation"""
        return 'Full NP Based Ring Buffer Object of size {}'.format(self.cap)


class RingBufferFull_List(RingBuff_List):
    def __repr__(self):
        """return string representation"""
        return 'Full List Based Ring Buffer Object of size {}'.format(self.cap)


class RingBufferFull_Deque(RingBuff_Deque):
    def __repr__(self):
        """return string representation"""
        return 'Full Deque Based Ring Buffer Object of size {}'.format(self.cap)
