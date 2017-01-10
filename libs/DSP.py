# -*- coding: utf-8 -*-

from collections import deque
import numpy as np
import itertools


def moving_average(iterable, n=3):
    """
    Boxcar or moving average implemented with the deque data type
    :param iterable:
    :param n:
    :return:
    """
    # moving_average([40, 30, 50, 46, 39, 44]) --> 40.0 42.0 45.0 43.0
    it = iter(iterable)
    d = deque(itertools.islice(it, n - 1))
    d.appendleft(0)
    s = sum(d)
    for elem in it:
        s += elem - d.popleft()
        d.append(elem)
        yield s / float(n)


def fft(data):
    """
    returns the positive half of the real-valued fft of the input signal
    :param data: the input signal to have the fft computed
    :return: the positive half of the real-valued fft of the input signal
    """
    return abs(np.fft.rfft(data)) / (len(data) / 2)


def fft_sample(data, sample_period):
    """
    returns the set of sample frequencies derivived from the fft of the given data with its defined sample period
    :param data: the input waveform of the signal
    :param sample_period: teh sample period time in seconds that the data was sampled at
    :return: list of values corresponding with the frequency bins of the fft
    """
    return np.fft.rfftfreq(len(data), sample_period)


def roll(data, shift, axis=None):
    return np.roll(data, shift, axis)
#
#
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
