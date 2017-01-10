# -*- coding: utf-8 -*-
# Copyright 2016 : Danyal Ahsanullah
from multiprocessing import Process, Array, Value
from Handlers.FileIOHandler import StreamWrite
from Handlers.SerialHandler import SerialHandler
from libs.Constants import *

""" Logging setup: """
import logging
from os import getcwd
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # CRITICAL , ERROR , WARNING , INFO , DEBUG , NOTSET
FH = logging.FileHandler('{}\\Debug\\debug.log'.format(getcwd()))
FMT = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
FH.setFormatter(FMT)
logger.addHandler(FH)


def serial_stream_local_time(params, time_buffer, start_log):
    SerialHandler(**params).stream_port_local_time(time_buffer, start_log)


def serial_stream_data(params):
    SerialHandler(**params).stream_port()


def serial_stream_data_time_inc(cls, params, time_buffer, start_log):
    cls(**params).stream_port_time_inc(time_buffer, start_log)


def write_op(kwargs, buf, time_buf, idx, lnth=CHUNKSIZE):
        StreamWrite(**kwargs, buffer=buf, time_buffer=time_buf).write(index=idx, length=lnth)


class ModeError(ValueError):
    """Error in operation mode setting for stream object"""


class Stream:
    """Stream handler object that handles streaming operations"""
    def __init__(self, cfg, func, index=Value('I', 0), **kwargs):
        self.buffer = Array('d', BUFFERSIZE)
        self.time_buffer = Array('d', BUFFERSIZE)
        self.mode = cfg.StreamType
        self.stream_enable = cfg.StreamEnable
        self.check = cfg.WriteEnable
        self.setup = kwargs
        self.start_log = Value('d', 0)  # holds values of start time to aid in plotting purposes
        self.index = index  # global index value passed between processes
        self.write = Process(target=write_op, name='Write_Proc',
                             args=(kwargs, self.buffer, self.time_buffer, self.index, self.index.value))
        if self.mode == STREAMTYPE.SERIAL:
            self.params = {'port_name': cfg.SerialPort,
                           'baudrate': cfg.SerialBaud,
                           # '_packet_size': cfg.PacketSize,
                           '_bit_order': cfg.BitOrder,
                           '_bit_depth': cfg.BitDepth,
                           'buffer': self.buffer,
                           'record_func': func,
                           'index': self.index,
                           'stream_enable': self.stream_enable
                           }
            self.stream = Process(target=serial_stream_local_time, name='Stream_proc_local_time',
                          args=(self.params, self.time_buffer, self.start_log))
            # self.stream = Process(target=serial_stream_data, name='Stream_proc', args=(self.params,))
        elif self.mode == STREAMTYPE.NI_DAQ:
            pass
        elif self.mode == STREAMTYPE.USB:
            pass
        else:
            raise ModeError('Incorrect Mode Value ({}) used...'.format(self.mode))

    def __str__(self):
        if self.mode == STREAMTYPE.SERIAL:
            return 'Stream Object in Serial Mode'
        elif self.mode == STREAMTYPE.NI_DAQ:
            return 'Stream Object in NI DAQ Mode'
        elif self.mode == STREAMTYPE.USB:
            return 'Stream Object in USB Mode'
        else:
            raise ModeError

    def __repr__(self):
        if self.mode == STREAMTYPE.SERIAL:
            return 'Stream Object in Serial Mode: ({})\nparams: \n{}'.format(self.mode, self.params)
        elif self.mode == STREAMTYPE.NI_DAQ:
            return 'Stream Object in NI DAQ Mode: ({})'.format(self.mode)
        elif self.mode == STREAMTYPE.USB:
            return 'Stream Object in USB Mode: ({})'.format(self.mode)
        else:
            raise ModeError

    def update_params(self, cfg):
        self.params['port_name'] = cfg.SerialPort
        self.params['baudrate'] = cfg.SerialBaud
        self.params['_bit_order'] = cfg.BitOrder
        self.params['_bit_depth'] = cfg.BitDepth

    def start_streaming(self):
        if not self.stream.is_alive():
            self.stream.start()
        else:
            pass

    def start_writing(self):
        if not self.check.value:
            self.check.value = True
        else:
            self.write.start()
        print('started')

    def stop_writing(self):
        self.check.value = False

        if self.write.is_alive():
            print('terminating')
            self.write.join()
        self.write = Process(target=write_op, name='Write_Proc',
                             args=(self.params, self.buffer, self.time_buffer, self.index, self.index.value))

    def stop_streaming(self):
        if self.check.value:
            self.check.value = False
        if self.stream.is_alive():

            try:
                self.stream_enable.value = False
                self.stream.join()
            except AssertionError:
                pass
        if self.mode == STREAMTYPE.SERIAL:
            # self.stream = Process(target=serial_stream_data, name='Stream_proc', args=(self.params,))
            self.stream = Process(target=serial_stream_local_time, name='Stream_proc_local_time',
                          args=(self.params, self.time_buffer, self.start_log))
        elif self.mode == STREAMTYPE.NI_DAQ:
            pass
        elif self.mode == STREAMTYPE.USB:
            pass
        else:
            raise ModeError('Incorrect Mode Value ({}) used...'.format(self.mode))

# Conditional check to start test
if __name__ == '__main__':
    import sys
    import time
    import templates.Stubs
    from templates.ConfigOptions import ConfigData
    # from pprint import pprint

    logger.info('starting...')
    par = templates.Stubs.Parent()
    con = ConfigData()
    idx = Value('I', 0)
    # templates.Stubs.app.exec_()
    from os import getcwd
    con.set_session_data(('Session1', getcwd()))
    con.set_serial_baud(9600)
    con.set_serial_port('COM4')
    con.BitDepth = BITDEPTHS.SIXTYFOUR
    con.set_stream_type(STREAMTYPE.SERIAL)
    con.set_stream_enable(True)
    con.write_block.value = True
    # con.set_write_enable(True)
    # logger.info('starting stream')
    test = Stream(cfg=con, func=par.update, config=con, index=idx,
                  choice=par.file_dup, update=par.session_name_update())
    # test.start_streaming()
    # time.sleep(1)
    # test.stop_streaming()
    #
    # logger.info('restarting test')
    time.sleep(1)

    # logger.info('starting stream')
    con.set_write_enable(True)
    print('starting stream')
    test.start_streaming()
    print('starting stream')
    time.sleep(1)
    # logger.info('starting write')
    print('starting write')
    test.start_writing()
    # logger.info('Disabling write')
    print('starting stream')
    time.sleep(10)
    # print('starting stream')
    print('Disabling write')
    con.write_block.value = False
    con.set_write_enable(False)
    print('Disabling stream')
    con.set_stream_enable(False)
    time.sleep(.5)
    # logger.info('closing')
    print('closing')
    test.stop_writing()
    test.stop_streaming()
    print('done')
    # print(repr(test))
    # pprint(vars(test))
    sys.exit(0)
