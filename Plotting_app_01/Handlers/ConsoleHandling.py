# -*- coding: utf-8 -*-
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.console
import sys

# """ Logging setup: """
# import logging
# from os import getcwd
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)  #  CRITICAL , ERROR , WARNING , INFO , DEBUG , NOTSET
# FH = logging.FileHandler('{}\\Debug\\debug.log'.format(getcwd()))
# FMT = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
# FH.setFormatter(FMT)
# logger.addHandler(FH)


# import data from plotting stuffs
# import data from files maybe?


class ConsoleHandler:
    def __init__(self):
        ## build an initial namespace for console commands to be executed in (this is optional;
        ## the user can always import these modules manually)
        namespace = {'pg': pg, 'np': np}

        ## initial text to display in the console
        text = """
        This is an interactive python console. The numpy and pyqtgraph modules have already been imported
        as 'np' and 'pg'.

        """

        self.console = pyqtgraph.console.ConsoleWidget(namespace=namespace, text=text)
        self.console.setWindowTitle('Logging App: ConsoleWidget')

    def start_console(self):
        self.console.show()



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        application = QtGui.QApplication(sys.argv)
        application.console = ConsoleHandler()
        application.console.start_console()
        sys.exit(application.exec_())

