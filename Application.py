# -*- coding: utf-8 -*-
"""
Application.py
Logging application main handler that handles interactions between the classes that makeup the application.
Copyright 2016 : Danyal Ahsanullah
"""
from Handlers.ConsoleHandling import ConsoleHandler
from Handlers.DialogHandler import StartSessionDialog, StartBitDepthDialog
from Handlers.GuiHandler import GuiHandler
from Handlers.StreamHandler import Stream
from templates.ConfigOptions import ConfigData
from libs.Constants import *
import multiprocessing as mp
import numpy as np
# from libs import DSP


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

'''Pipe object between main and stream''' # todo maybe move into main Handler?
p_rx, p_tx = mp.Pipe()


class MainHandler(GuiHandler):
    """
    The main handling class that controls interactions between components of the application
    Responsible for starting and stopping remote processes as well as coordinating data transfer between them
    """
    # More or Less Finalised:
    def __init__(self):
        """
        creates the main parts of the application
        """
        # self.p_rx, self.p_tx = mp.Pipe()
        self.Config = ConfigData()
        super(MainHandler, self).__init__(self)
        self.index = mp.Value('I', 0)
        self.pipe = p_rx
        self.stream = Stream(cfg=self.Config, pipe=p_tx, index=self.index, choice=self.file_dup,
                             update=self.session_name_update, config=self.Config)
        logger.info('initial window title is: {}'.format(self.MainWindow.windowTitle()))
        self.session_name_update()
        self.update_bit_data()
        # todo, change this to something else probably
        self.data_set = np.zeros(shape=(WINDOWSIZE, 2), dtype=np.float64)
        self.console = ConsoleHandler()

    # def update(self, cfg, index, delta, chunk_length=CHUNKSIZE, stream=None):
    #     logger.info('update')
    #     cfg.write_block.value = True
    #     # record data
    #     start = index - chunk_length
    #     self.data_set = append(self.data_set, concatenate((stream.buffer[start:index],
    #                                    stream.time_buffer[start:index])).reshape((2, chunk_length)), axis=1)
    #     self.index += chunk_length
    #     # plot additional data down...
    #     self.main_plot.plot(x=self.data_set[0], y=self.data_set[1], clear=True, _callSync='off')
    #     self.second_plot.plot(x=DSP.fft_sample(self.data_set[1], delta), y=DSP.fft(self.data_set[1]),
    #                      clear=True, _callSync='off')

    def session_name_update(self):
        """
        Gets Updated Session Name from Session Name Dialog Box
        Called from the actionNameSession QAction
        """
        name, path = StartSessionDialog(self.Config).get_session_values()
        self.Config.set_session_data(_name=name, _path=path)
        self.MainWindow.setWindowTitle('Logging App - {}'.format(self.Config.get_session_data()[0]))
        logger.info('window title is: {}'.format(self.MainWindow.windowTitle()))

    def update_bit_data(self):
        """
        Updates Configuration Bitdata values based from BitDepth Dialog
        """
        bit_data = StartBitDepthDialog(self.Config).get_bit_values()
        self.Config.set_bit_data(bit_data)

    def update_serial_config(self):
        """
        Updates Serial Configuration parameters
        """
        # logger.info('serial cfg updated')
        from re import search
        port = search('^(\S+)', self.PortDropDown.currentText())
        self.Config.SerialPort = port.group(1) if (port is not None) else None
        self.Config.SerialBaud = int(self.BaudDropDown.currentText())
        self.stream.update_params(self.Config)
        logger.info(self.Config.SerialPort)
        logger.info(self.PortDropDown.currentIndex())
        logger.info(self.PortDropDown.currentText())

    def open_console(self):
        """ Opens an interactive Python Console """
        # NOTE: MAY WANT TO INTEGRATE AS A DEBUG CONSOLE?
        logger.info('Console Launched')
        self.console.start_console()

    # Almost Good:
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

    def close_app(self):
        """
        Exits Application
        Called from the actionExit QAction
        """
        logger.info('Closing Application session: {}'.format(self.Config.get_session_data()[0]))
        current = mp.current_process()
        children = mp.active_children()
        logger.info('Active children: {}'.format(children))
        for process in children:
            logger.info('terminating process: {} ({})'.format(process.name, process.pid))
            process.terminate()
            process.join(timeout=1.0)
        logger.info('Exiting Main Process: {} ({})'.format(current.name, current.pid))
        self.close_win()
        # sys.exit(0)

# ... its a mess right now:
    def update(self):
        if self.pipe.poll():
            try:
                self.Config.write_block.value = True
                buf = self.pipe.recv()
                logger.info('buffer[0] = {}'.format(buf[0]))
                # self.data_set = concatenate([self.data_set, buf])
                self.data_set = np.append(self.data_set, buf)
                self.main_plot.plot(self.data_set, clear=False, _callSync='off')
                # x=range(0, len(self.data_set)), clipToView=True)
            except EOFError:
                logger.info('EOFError')
                pass
# END CLASS

# Conditional check to start application and provide safeguard for multiprocessing
if __name__ == '__main__':
    import sys
    from pyqtgraph.Qt import QtGui
    import atexit
    mp.freeze_support()
    app = QtGui.QApplication(sys.argv)
    MainHandle = MainHandler()
    atexit.register(MainHandle.close_app)
    # app.exit()
    app.exec_()
    # sys.exit(app.exec_())
    # logger.info('safely closed')
    sys.exit(0)
