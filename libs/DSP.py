# -*- coding: utf-8 -*-

from collections import deque
import numpy as np
import itertools


# """ Logging setup: """
# import logging
# import os
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)  # CRITICAL , ERROR , WARNING , INFO , DEBUG , NOTSET
# if not os.path.isdir('{}\\Debug'.format(os.getcwd())) and (logger.level is not logger.disabled):
#     os.mkdir('{}\\Debug'.format(os.getcwd()))
# FH = logging.FileHandler('{}\\Debug\\debug.log'.format(os.getcwd()))
# FMT = logging.Formatter("%(asctime)s - %(name)s -- %(message)s")
# FH.setFormatter(FMT)
# logger.addHandler(FH)

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


def calc_delta(data) -> float:
    """
    returns the average delta value for closely spaced data sets
    :param data: array of time values to have the average timestep be computed for
    :return: average timestep value
    """
    return np.diff(data).sum() / len(data)


def roll(data, shift, axis=None):
    return np.roll(data, shift, axis)
