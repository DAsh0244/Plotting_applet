# -*- coding: utf-8 -*-
# FileIOHandler.py
# Creates a File to write stream data to while streaming
# Copyright 2016 : Danyal Ahsanullah
from libs.Constants import *

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


class StreamWrite:
    """
        --Handles Writing streamed data to files--
    Makes a local copy of the relevant configuration options and
    writes the specified output format file of the incoming stream data
    until global config option StreamEnable == False
    """
    def __init__(self, config, choice, session_update, buffer, time_buffer):
        """
        :param config: configData class object
        :param choice:
        :param session_update:
        :param buffer:
        :param time_buffer:
        """
        super(StreamWrite, self).__init__()
        import os
        self.fileType, self.fileName, self.path, self.fileNum = config.get_file_data()
        self.enable = config.WriteEnable
        self.choice = choice
        self.write_block = config.write_block
        for i in os.listdir(self.path):
            if self.fileName == (os.path.splitext(i)[0]).split(sep='-')[0]:
                logger.info('File(s) Already exists.')
                if self.choice():
                    self.fileName = session_update()
                    logger.info('Session Renamed!')
                else:
                    self.fileNum += 1
                    logger.info('FileNum = {}'.format(self.fileNum))
                    # config.WriteNum += 1  #  maybe update on destruction of StreamWrite
        if self.fileType == EXTENSION.TXT:
            self.write_params = {'ext': 'txt', 'delim': ' ', 'data': (buffer, time_buffer)}
        elif self.fileType == EXTENSION.CSV:
            self.write_params = {'ext': 'csv', 'delim': ',', 'data': (buffer, time_buffer)}
        elif self.fileType == EXTENSION.MAT:
            self.write_params = {'ext': 'mat', 'delim': ' ', 'data': (buffer, time_buffer)}
        else:
            logger.info('ERROR, non matching file type {}'.format(self.fileType))

    # def __del__(self):
        # logger.info('Deleting instance...')

    #  TODO Fix this to being a proper logging function
    def write(self, index, length=CHUNKSIZE):
        """
        writes up to two columns of text in a single file in the formats described in libs.Constants.EXTENSION
        data is passed to it in hte FileIO handler __intit__ method, and is then used to write a double column data set
        writing occurs in blocks whenever the plot update function is called, therefore making hte default write length
        the last libs.Constants.CHUNKSIZE entries written save for a premature termination, in which the value to
        of length is the number of entries to read from.
        """
        from time import time
        logger.info('writing text file...')
        t1 = time()
        try:
            file = '{}-{}.{}'.format(self.fileName, self.fileNum, self.write_params['ext'])
            with open(file, 'w') as f:
                while self.enable.value:
                    if self.write_block.value:
                        val1 = self.write_params['data'][0][(index.value-length):index.value+1]
                        val2 = self.write_params['data'][1][(index.value-length):index.value+1]
                        for (i, j) in zip(val1, val2):
                            f.write('{}{}{}\n'.format(i, self.write_params['delim'], j))
                            logger.info('log data: {}  {}'.format(i, j))
                        logger.info('Block Written')
                        self.write_block.value = False
            logger.info('{} Done! \"{}\"...Time Taken: {}sec'.format(self.write_params['ext'].upper(), file,
                                                                     str(time() - t1)))
        except AttributeError:
            logger.info('Bad Initialisation')
        # sys.exit()
        # pass

#  TEST Config setup for ensuring shared mem can kill process
if __name__ == '__main__':
    from templates import Stubs
    from templates.ConfigOptions import ConfigData
    from multiprocessing import Process
    import os
    import sys

    time_buff = os.urandom(1024)
    buff = os.urandom(1024)
    idx = 0
    cfg = ConfigData()
    if not os.path.isdir('{}\\OUTPUT'.format(os.getcwd())):
        os.mkdir('{}\\OUTPUT'.format(os.getcwd()))
    cfg.set_session_data('test_01', '{}\\OUTPUT'.format(os.getcwd()))
    cfg.WriteEnable.value = True
    par = Stubs.Parent
    kill = Process(target=par.disable, args=(cfg,))
    main_window = Stubs.MainWindow(par, kill.start)
    stream = Process(target=StreamWrite(cfg, par.file_dup, par.session_name_update, buff, time_buff).write, args=(idx,))
    stream.start()
    Stubs.app.exec_()
    # main_window.hide()
    Stubs.app.exit()
    stream.join(timeout=15)
    if stream.is_alive():
        stream.terminate()
        stream.join(timeout=5)
    sys.exit(0)
