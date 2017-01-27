# -*- coding: utf-8 -*-
# Copyright 2016 : Danyal Ahsanullah

from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *

""" Logging setup: """
import logging
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # CRITICAL , ERROR , WARNING , INFO , DEBUG , NOTSET
if not os.path.isdir('{}\\Debug'.format(os.getcwd())) and (logger.level is not logger.disabled):
    os.mkdir('{}\\Debug'.format(os.getcwd()))
FH = logging.FileHandler('{}\\Debug\\debug.log'.format(os.getcwd()))
FMT = logging.Formatter("%(asctime)s - %(name)s -- %(message)s")
FH.setFormatter(FMT)
logger.addHandler(FH)


class AnalogInput(object):
    def __init__(self, channel, limit=None, reset=False):
        self.taskHandle = None
        if isinstance(channel, str):
            self.channel = [channel]
        else:
            self.channel = channel
        if limit is None:
            self.limit = (-10.0, 10.0)
        elif isinstance(limit, tuple):
            self.limit = limit
        else:
            raise TypeError('Invalid type{}. Type must be either <None> or <tuple>'.format(type(limt)))

        if reset:
            DAQmxResetDevice(physicalChannel[0].split('/')[0])

    def configure(self):
        pass

    def read(self, values):
        pass


class MultiChannelAnalogInput(object):
    """Class to create a multi-channel analog input

    Usage: AI = MultiChannelInput(physicalChannel)
        physicalChannel: a string or a list of strings
    optional parameter: limit: tuple or list of tuples, the AI limit values
                        reset: Boolean
    Methods:
        read(name), return the value of the input name
        readAll(), return a dictionary name:value
    """

    def __init__(self, physical_channel, limit=None, reset=False):
        self.taskHandles = None
        if type(physical_channel) == type(""):
            self.physicalChannel = [physical_channel]
        else:
            self.physicalChannel = physical_channel
        self.numberOfChannel = physical_channel.__len__()
        if limit is None:
            self.limit = dict([(name, (-10.0, 10.0)) for name in self.physicalChannel])
        elif type(limit) == tuple:
            self.limit = dict([(name, limit) for name in self.physicalChannel])
        else:
            self.limit = dict([(name, limit[i]) for i, name in enumerate(self.physicalChannel)])
        if reset:
            DAQmxResetDevice(physical_channel[0].split('/')[0])

    def configure(self):
        # Create one task handle per Channel
        taskHandles = dict([(name, TaskHandle(0)) for name in self.physicalChannel])
        for name in self.physicalChannel:
            DAQmxCreateTask("", byref(taskHandles[name]))
            DAQmxCreateAIVoltageChan(taskHandles[name], name, "", DAQmx_Val_RSE,
                                     self.limit[name][0], self.limit[name][1],
                                     DAQmx_Val_Volts, None)
        self.taskHandles = taskHandles

    def readAll(self):
        return dict([(name, self.read(name)) for name in self.physicalChannel])

    def read(self, name=None):
        if name is None:
            name = self.physicalChannel[0]
        taskHandle = self.taskHandles[name]
        DAQmxStartTask(taskHandle)
        data = numpy.zeros((1,), dtype=numpy.float64)
        #        data = AI_data_type()
        read = int32()
        DAQmxReadAnalogF64(taskHandle, 1, 10.0, DAQmx_Val_GroupByChannel, data, 1, byref(read), None)
        DAQmxStopTask(taskHandle)
        return data[0]


if __name__ == '__main__':
    multipleAI = MultiChannelAnalogInput([b"Dev1/ai2", b"Dev1/ai1"])
    multipleAI.configure()
