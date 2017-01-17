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
    returns the set of sample frequencies derived from the fft of the given data with its defined sample period
    :param data: the input waveform of the signal
    :param sample_period: teh sample period time in seconds that the data was sampled at
    :return: list of values corresponding with the frequency bins of the fft
    """
    return np.fft.rfftfreq(len(data), sample_period)


def roll(data, shift, axis=None):
    return np.roll(data, shift, axis)
