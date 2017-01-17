# -*- coding: utf-8 -*-
# Copyright 2016 : Danyal Ahsanullah

import sys
from re import search
from numpy import diff, array, concatenate, frombuffer
from libs import fakeSerial as serial
# import serial
from libs.Constants import *

""" Logging setup: """
import logging
from os import getcwd
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  #  CRITICAL , ERROR , WARNING , INFO , DEBUG , NOTSET
FH = logging.FileHandler('{}\\Debug\\debug.log'.format(getcwd()))
FMT = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
FH.setFormatter(FMT)
logger.addHandler(FH)


def try_open_port(_port):
    ret = False
    test = serial.Serial(timeout=1, writeTimeout=1)
    test.port = _port
    try:
        test.open()
        if test.isOpen():
            test.close()
            ret = True
    except serial.serialutil.SerialException:
        logger.error('Failed to open port "{}"'.format(_port))
    return ret


def check_baud(current_baud):
    if current_baud in serial.Serial.BAUDRATES:
        logger.info('Baud OK!')
        return True
    else:
        logger.info('Baud Check Failed!')
        return False


def check_com(current_port, current_baud):
    # module_logger.info (current_port)
    # module_logger.info (len(current_port))
    # module_logger.info (re.search('^([\w]+)', self.PortDropDown.currentText()).group(1),)
    if len(current_port) == 0:
        logger.info('Empty Port Name!')
        pass
    elif check_baud(current_baud):
        port = search('^(\S*)', current_port).group(1)
        if try_open_port(port):
            logger.info('{}: Port OK!'.format(port))
            return True
        else:
            logger.info('{}: Check Failed!'.format(port))
            return False


def ports_scan():
    """
    Scans for ports and returns a list of currently available ports as a list
    :return: a list of current ports found by the scan.
    """
    import serial.tools.list_ports
    # ports = list(serial.tools.list_ports.comports())
    ports = list(serial.tools.list_ports.comports())
    # ports = list(serial.tools.list_ports.comports())
    logger.info('Scanning for Ports...')
    if ports:
        logger.info('Ports Found:')
        for p in ports:
            logger.info(str(p))
        return ports
    else:
        logger.info('No Ports Found!')
        return ''


class SimulatedValue:
    def __init__(self, state=False):
        self.value = state


class SerialHandler(serial.Serial):
    def __init__(self, pipe=None, port_name=None, stream_enable=SimulatedValue(False), buffer=None, index=0,
                 _bit_order=BITORDER.LSB, _bit_depth=BITDEPTHS.EIGHT, _packet_size=8, **kwargs):
        super(SerialHandler, self).__init__(**kwargs)
        self.buf = buffer
        self.time_buf = None
        self.data_size = _bit_depth
        self.enable = stream_enable
        self.packet = _packet_size
        self.order = _bit_order  # not for serial communication but for non PHY level protocols
        self.pipe = pipe
        self.index = index
        self.port = port_name

    def start_com(self):
        if not check_com(self.port, self.baudrate):
            logger.info('Port: {} failed com port check {}'.format(self.port, ''))
            return False
        else:
            if not self.isOpen():
                self.open()
            return True

    def stream_port(self):
        """
        handles streaming of a port with no time data sent over serial packets and no local time stamping occurring
        closes on TypeError when serial data is no longer able to be read.
        :return:
        """
        from multiprocessing import current_process
        proc = current_process()
        logger.info('PROCESS NAME: ' + str(proc.name))
        logger.info('PROCESS PID: ' + str(proc.pid))
        if not self.start_com():
            pass
            logger.info('Stream Cancelled')
        else:
            if not self.isOpen():
                self.open()
            i = 0
            try:
                from math import ceil
                from ctypes import c_double
                from struct import unpack
                num_bytes = ceil(self.data_size/self.bytesize)
                logger.info('\ndata size: {}\nbytesize: {}\nnumber of bytes to read: {}'
                            .format(self.data_size, self.bytesize, num_bytes))
                while self.enable.value:
                    ret = self.read(num_bytes)
                    offset = num_bytes - len(ret)
                    if offset > 0:
                        ret += "\0" * offset
                    # TODO HANDLE REBUILDING DATA FROM BYTES -- LSB/MSB first
                    # TODO - Ring Buffers definetly
                    temp = unpack('f', ret)     # TODO correct format specification somehow
                    self.buf[i] = temp[0]
                    if (i % CHUNKSIZE == 0 and i != 0) or (i == BUFFERSIZE-1):
                        self.pipe.send(self.buf[i-CHUNKSIZE:i])
                #  data = self.ser.read(size=(math.ceil(self.data_size/8)))
                #  module_logger.info(data)
                    i = 0 if i == BUFFERSIZE-1 else (i+1)  # i == BUFFERSIZE ? i = 0 : i++
            except TypeError:
                i -= 1
                logger.info('Finished reading...Index = {}'.format(i))
            finally:
                self.pipe.send(self.buf[i-CHUNKSIZE:i])
                logger.info('Array Contents:')
                for entry in range(0, BUFFERSIZE):
                    logger.info('{}: {}'.format(entry, self.buf[entry]))
                self.close()
                logger.info('closed self')
        # sys.exit(0)

    def stream_port_local_time(self, time_buf, start):
        """
        handles streaming of a port with no time data sent over serial packets and  local time stamping occurring
        closes on TypeError when serial data is no longer able to be read.
        :return:
        """
        from time import perf_counter, time
        self.time_buf = time_buf
        from multiprocessing import current_process
        proc = current_process()
        logger.info('PROCESS NAME: ' + str(proc.name))
        logger.info('PROCESS PID: ' + str(proc.pid))
        if not self.start_com():
            pass
            logger.info('Stream Cancelled')
        else:
            self.index.value = 0
            try:
                from math import ceil
                from struct import unpack
                num_bytes = ceil(self.data_size/self.bytesize)
                start.value = time()
                while self.enable.value:
                    ret = self.read(num_bytes)
                    if len(ret) == 0:
                        raise TypeError
                    # module_logger.info(ret)
                    offset = num_bytes - len(ret)
                    if offset > 0:
                        ret += bytearray([0] * offset)
                    # TODO HANDLE REBUILDING DATA FROM BYTES -- LSB/MSB first
                    self.buf[self.index.value] = unpack('d', ret)[0]
                    self.time_buf[self.index.value] = perf_counter()
                    logger.info('{}: {} , {}'.format(self.index.value,
                                                     self.buf[self.index.value],
                                                     self.time_buf[self.index.value]))
                    # index != BUFFERSIZE ? index++ : index = 0;
                    self.index.value = self.index.value + 1 if self.index.value != BUFFERSIZE-1 else 0
                    if self.index.value % CHUNKSIZE == 0 and self.index.value != 0:
                        a = array(self.time_buf[self.index.value-CHUNKSIZE:self.index.value])
                        delta = diff(a).sum() / CHUNKSIZE
                        self.pipe.send(self.index.value)
                        self.pipe.send(delta)
            except TypeError:
                pass
            finally:
                self.index.value = self.index.value-1 if self.index.value != 0 else BUFFERSIZE-1
                # TODO - Ring Buffers Anyone?
                tem_val = frombuffer(self.buf.get_obj())
                tem_time = frombuffer(self.time_buf.get_obj())
                logger.info('Finished reading...Index = {}'.format(self.index.value))
                if CHUNKSIZE - 1 < self.index.value <= BUFFERSIZE - 1:
                    a = array(self.time_buf[self.index.value - CHUNKSIZE:self.index.value])
                elif self.index.value < CHUNKSIZE - 1:
                    a = array(tem_time[:self.index.value])
                delta = diff(a).sum() / CHUNKSIZE
                logger.info('{}  {}  {}'.format(self.index.value, delta, self.index.value))
                self.pipe(self.index.value, delta, self.index.value)
                self.close()
                self.buf.__setslice__(0, BUFFERSIZE,
                                    concatenate([tem_val[self.index.value + 1:BUFFERSIZE], tem_val[:self.index.value + 1]]))
                self.time_buf.__setslice__(0, BUFFERSIZE, (concatenate([tem_time[self.index.value + 1:BUFFERSIZE],
                                                                        tem_time[:self.index.value + 1]])
                                                           - tem_time[self.index.value + 1])
                                           )
                logger.info('closed self')
            # sys.exit(0)
#
# #todo implement this proper
#     def stream_port_sent_time(self, time_buf=None):
#         """
#         handles streaming of a port with no time data sent over serial packets and  local time stamping occurring
#         closes on TypeError when serial data is no longer able to be read.
#         :return:
#         """
#         from multiprocessing import current_process
#         proc = current_process()
#         module_logger.info('PROCESS NAME: ' + str(proc.name))
#         module_logger.info('PROCESS PID: ' + str(proc.pid))
#         if not self.start_com():
#             module_logger.info('Stream Cancelled')
#         else:
#             try:
#                 from math import ceil
#                 from ctypes import c_double
#                 from struct import unpack
#                 i = 0
#                 num_bytes = ceil(self.data_size/self.bytesize)
#                 while i < BUFFERSIZE:
#                     ret = self.read(num_bytes)
#                     offset = num_bytes - len(ret)
#                     if offset > 0:
#                         ret += "\0" * offset
#                     # TODO HANDLE REBUILDING DATA FROM BYTES -- LSB/MSB first
#                     self.buf[i] = unpack('d', ret)[0]
#                     i = 0 if i == BUFFERSIZE-1 else i+1  # i == BUFFERSIZE ? i = 0 : i++
#                     if i % CHUNKSIZE == 0:
#                         self.trigger_update(True)
#                         module_logger.info('{}: {}'.format(i, self.buf[i]))
#                 #  data = self.ser.read(size=(math.ceil(self.data_size/8)))
#                 #  module_logger.info(data)
#             except TypeError:
#                 module_logger.info('Finished reading...Index = {}'.format(i-1))
#             # module_logger.info('Array Contents:')
#             # for i in range(0, BUFFERSIZE):
#             #     if i % 100 == 0:
#             #         module_logger.info('{}: {}'.format(i, self.buf[i]))
#             self.close()
#             module_logger.info('closed self')
#         # sys.exit(0)
#

if __name__ == '__main__':
    from multiprocessing import Array, Process, Value  # ,freeze_support
    # freeze_support()
    # module_logger.info('test')
    # # c = ports_scan()
    # # while not c:
    # #     c = ports_scan()
    params = {'port_name': 'COM4',
              'baudrate': 9600,
              '_packet_size': 8,
              '_bit_order': BITORDER.LSB,
              '_bit_depth': BITDEPTHS.SIXTYFOUR,
              'buffer': Array('d', BUFFERSIZE),
              'record_func': lambda c, y, z=None: logger.info('\n\t\t\t\t\t\t\t\t\t\t{}  {}  {}\n\n'.format(c, y, z)),
              'index': Value('I', 0)
              }
    time_set = Array('d', BUFFERSIZE)
    start_time = Value('d')
    x = Process(target=SerialHandler(**params).stream_port_local_time(time_set, start_time))
    x.start()
    from time import sleep
    sleep(2)
    x.join()
    logger.info('Contents')
    for i in range(0, BUFFERSIZE):
        logger.info('{}: {} , {}'.format(i, params['buffer'][i], time_set[i]))
    sys.exit(0)
