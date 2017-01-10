# -*- coding: utf-8 -*-
"""
Application.py
Logging application main handler that handles interactions between the classes that makeup the application.
Copyright 2016 : Danyal Ahsanullah
"""
from multiprocessing import current_process, active_children, Value
from Handlers.ConsoleHandling import ConsoleHandler
from Handlers.DialogHandler import StartSessionDialog, StartBitDepthDialog
from Handlers.GuiHandler import GuiHandler
from numpy import zeros, float64, append, concatenate
from Handlers.StreamHandler import Stream
from libs import DSP
from libs.Constants import CHUNKSIZE
from templates.ConfigOptions import ConfigData
# from Handlers.FileIOHandler import StreamWrite

""" Logging setup: """
import logging
from os import getcwd
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # CRITICAL , ERROR , WARNING , INFO , DEBUG , NOTSET
FH = logging.FileHandler('{}\\Debug\\debug.log'.format(getcwd()))
FMT = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
FH.setFormatter(FMT)
logger.addHandler(FH)
logger.info('************************ PROGRAM STARTED ************************')


def update(*args, **kwargs):
    MainHandler.update(*args, **kwargs)

data_set = zeros(shape=(0, 2), dtype=float64)
idx = Value('I', 0)


class MainHandler(GuiHandler):
    """
    The main handling class that controls interactions between components of the application
    Responsible for starting and stopping remote processes as well as coordinating data transfer between them
    """
    # More or Less Finalised:
    def __init__(self):
        self.Config = ConfigData()
        super(MainHandler, self).__init__(self)
        # self.index = 0
        global idx
        self.stream = Stream(cfg=self.Config, func=(update, ), index=idx, choice=self.file_dup,
                             update=self.session_name_update, config=self.Config)
        # self.write = StreamWrite(choice=self.file_dup, update=self.session_name_update, config=self.Config)
        logger.info('initial window title is: {}'.format(self.MainWindow.windowTitle()))
        self.session_name_update()
        self.update_bit_data()
        # data init - will hold total set of data for the incoming waveforms

        logger.info('Bit Depth: {}'.format(str(self.Config.BitDepth)))

    #TODO Figure out how to fix this.... its the rate limiting step here it seems
    @staticmethod
    def update(cfg, index, delta, chunk_length=CHUNKSIZE, main_plot=None, second_plot=None, stream=None):
        """
        Called when a new chunk of data has been read by the stream.

        :param cfg: parent Config object. MUST be passed in initialisation of the stream object.
        :param index: current stream buffer index
        :param delta: calculated average time step between points of the stream buffer
        :param chunk_length: number of entries to be added to the plot, most use cases should be CHUNKSIZE
        :param main_plot: the main plot that handles time domain data
        :param second_plot: the secondary plot that handles the FFT data of the data set
        :param stream object to get at its buffers

        :return: N/A
        """
        logger.info('update')
        global data_set
        global idx
        cfg.write_block.value = True
        # record data
        start = index - chunk_length
        data_set = append(data_set,
                          concatenate((stream.buffer[start:index],
                                       stream.time_buffer[start:index])).reshape((2, chunk_length)),
                          axis=1)
        idx += chunk_length
        # plot additional data down...
        main_plot.plot(x=data_set[0], y=data_set[1], clear=True, _callSync='off')
        second_plot.plot(x=DSP.fft_sample(data_set[1], delta), y=DSP.fft(data_set[0]), clear=True, _callSync='off')

    def session_name_update(self):
        """
        Gets Updated Session Name from Session Name Dialog Box
        Called from the actionNameSession QAction
        """
        self.Config.set_session_data(StartSessionDialog(self.Config).get_session_values())
        self.MainWindow.setWindowTitle('Logging App - {}'.format(self.Config.get_session_data()[0]))
        logger.info('window title is: {}'.format(self.MainWindow.windowTitle()))

# TODO MOVE DEBUG FUNCIONALITY
    def open_console(self):
        """ Opens an interactive Python Console """
        # NOTE: MAY WANT TO INTEGRATE AS A DEBUG CONSOLE?
        # from pprint import pprint
        # pprint(vars(self.Config))
        # pprint(vars(self.stream))
        # noinspection PyAttributeOutsideInit
        self.console = ConsoleHandler()
        logger.info('Console Launched')
        self.console.start_console()

    # Almost Good:
    def toggle_write(self):
        """
        Enables Remote Process to start steaming port data
        Called by the WriteButton QPushButton
        """
        if self.Config.StreamEnable.value:
            self.toggle_write_state()
            self.stream.update_params(self.Config)
            if not self.Config.WriteEnable.value:
                self.Config.WriteEnable.value = True
                self.stream.start_writing()
            else:
                self.Config.WriteEnable.value = False
                self.stream.stop_writing()

    def toggle_plotting(self):
        """
        Enables Remote Process to start steaming port data
        Called by the openPort QPushButton
        """
        self.toggle_plot_state()
        self.update_serial_config()
        self.stream.update_params(self.Config)
        if not self.Config.StreamEnable.value:
            self.Config.StreamEnable.value = True
            if not self.stream.stream.is_alive():
                self.stream.start_streaming()
        else:
            self.Config.StreamEnable.value = False
            if self.stream.stream.is_alive():
                self.stream.stop_streaming()
            self.Config.WriteEnable.value = False
            self.toggle_write()

# ... its a mess right now:
    def update_serial_config(self):
        logger.info('triggered')
        from re import search
        port = search('^(\S+)', self.PortDropDown.currentText())
        self.Config.SerialPort = port.group(1) if (port is not None) else None
        self.Config.SerialBaud = int(self.BaudDropDown.currentText())
        self.stream.update_params(self.Config)
        logger.info(self.Config.SerialPort)
        logger.info(self.PortDropDown.currentIndex())
        logger.info(self.PortDropDown.currentText())

    def close_app(self):
        """
        Exits Application
        Called from the actionExit QAction
        """
        logger.info('Closing Application session: {}'.format(self.Config.get_session_data()[0]))
        logger.info('Active children: {}'.format(active_children()))
        for process in active_children():
            logger.info('terminating process: {} ({})'.format(process.name, process.pid))
            process.terminate()
            process.join(timeout=1.0)
        current = current_process()
        logger.info('Exiting Main Process: {} ({})'.format(current.name, current.pid))
        # print(self.parent)
        self.close_win()

        # sys.exit(0)

    def update_bit_data(self):
        bit_data = StartBitDepthDialog(self.Config).get_bit_values()
        self.Config.set_bit_data(bit_data)
# END CLASS

# Conditional check to start application and provide safeguard for multiprocessing
if __name__ == '__main__':
    import sys
    from pyqtgraph.Qt import QtGui
    # from multiprocessing import freeze_support
    # freeze_support()
    app = QtGui.QApplication(sys.argv)
    MainHandle = MainHandler()
    # app.exit()
    app.exec_()
    # print('safely closed')
    sys.exit(0)
