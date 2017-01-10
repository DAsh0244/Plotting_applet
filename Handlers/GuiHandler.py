# -*- coding: utf-8 -*-
# Copyright 2016 : Danyal Ahsanullah

from PyQt4 import QtGui
from Handlers.SerialHandler import SerialHandler, ports_scan
from templates.Plotting_Gui import Ui_Plotting_Gui

# """ Logging setup: """
# import logging
# from os import getcwd
# # logger = logging.get# logger(__name__)
# # logger.setLevel(logging.INFO)  #  CRITICAL , ERROR , WARNING , INFO , DEBUG , NOTSET
# FH = logging.FileHandler('{}\\Debug\\debug.log'.format(getcwd()))
# FMT = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
# FH.setFormatter(FMT)
# # logger.addHandler(FH)
# try:
#     #
#     _fromUtf8 = QtCore.QString.fromUtf8
# except AttributeError:
#     def _fromUtf8(s):
#         return s
try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class GuiHandler(Ui_Plotting_Gui):
    def __init__(self, par):
        super(GuiHandler, self).__init__()

        # flag vars for keeping track of toggle state buttons
        self.open_port = False
        self.fft_enable = False
        self.write_checked = False

        # bulk of the Gui init
        self.MainWindow = QtGui.QMainWindow()
        self.setupUi(self.MainWindow)

        # hide second plot
        self.Plot_2.hide()

        # setup action groups for exclusivity between options
        self.extensions = QtGui.QActionGroup(self.menubar)      # creates action group for file check boxes
        self.order = QtGui.QActionGroup(self.menubar)           # creates action group for MSB/LSB
        self.axis = QtGui.QActionGroup(self.menubar)            # creates action group for Combined/Separate axis
        self.mode = QtGui.QActionGroup(self.menubar)            # creates action group for mode

        # get possible baud rates and populate baud selection box with values - search for possible com ports
        baud = SerialHandler().BAUDRATES
        self.BaudDropDown.addItems([str(e) for e in baud])      # add baudrates list as options
        self.BaudDropDown.setCurrentIndex(baud.index(9600))     # makes '9600' default option
        self.BaudDropDown.setValidator(QtGui.QIntValidator(baud[0], baud[-1]))  # set max/min to have in box
        self.update_com_ports()     # searches for com ports and populates a list of them in the cop port selection box

        # menu init
        self.actionScan_Ports.triggered.connect(self.update_com_ports)
        self.actionExit.triggered.connect(par.close_app)
        self.actionNameSession.triggered.connect(par.session_name_update)
        self.actionInput_Bit_Depth.triggered.connect(par.update_bit_data)
        self.actionConsole.triggered.connect(par.open_console)
        self.extensions.addAction(self.actionCSV)
        self.extensions.addAction(self.actionTXT)
        self.extensions.addAction(self.actionMAT)
        self.order.addAction(self.actionLSB_first)
        self.order.addAction(self.actionMSB_first)
        self.axis.addAction(self.actionSeperate_Axis)
        self.axis.addAction(self.actionCombined_Axis)
        self.mode.addAction(self.actionSerial)
        self.mode.addAction(self.actionNI_DAQ)
        self.mode.addAction(self.actionUSB)

        # button init
        self.DualPlot.stateChanged.connect(self.dual_plot)
        self.FFT_button.clicked.connect(self.toggle_fft_state)
        self.Plot_Button.clicked.connect(par.toggle_plotting)
        self.Write_Button.clicked.connect(par.toggle_write)
        self.PortDropDown.currentIndexChanged.connect(par.update_serial_config)
        self.BaudDropDown.currentIndexChanged.connect(par.update_serial_config)


        # self.timebuffer = zeros(shape=CHUNKSIZE * MAXCHUNKS, dtype=float64)

        # First Plot Setup
        self.main_plot = self.Plot_1.pg.PlotItem()
        self.main_plot.showGrid(x=True, y=True)
        self.main_plot.setLabel('bottom', 'Time', 's')
        self.main_plot.setLabel('left', 'Voltage', 'V')
        self.main_plot.setXRange(-1, 0.5)
        self.main_plot._setProxyOptions(deferGetattr=True, callSync='off')
        self.Plot_1.setCentralItem(self.main_plot)

        # Second Plot Setup
        self.second_plot = self.Plot_2.pg.PlotItem()
        self.second_plot.showGrid(x=True, y=True)
        self.second_plot.setLabel('bottom', 'freq', 'Hz')
        self.second_plot.setLabel('left', 'magnitude', 'dB')
        self.second_plot._setProxyOptions(deferGetattr=True, callSync='off')
        self.Plot_2.setCentralItem(self.second_plot)

        # Optional Line for now
        # self.main_plot.plot(x=self.timebuffer, y=self.databuffer,  callSync='off')
        # self.second_plot.plot(x=DSP.fft_sample(self.databuffer, Dummy_Data.delta), y=DSP.fft(self.databuffer),
        #                       callSync='off')

        self.MainWindow.show()

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(par.update)
        # self.timer.start(50)

    #  END INIT

    def dual_plot(self):
        """
        Enables Both Plots to be shown at once
        Called when 'DualPlot' checkbutton is checked
        """
        if self.DualPlot.isChecked():
            # logger.warning('Button Checked!')
            self.Plot_1.show()
            self.Plot_2.show()
        else:
            # logger.warning('Button Not Checked!')
            self.Plot_2.hide()

    def update_com_ports(self):
        """
        Calls the SerialHandler.ports_scan method
            to get a list of current ports and updates 'PortDropDown' with new list
        Called from the actionScan_Ports QAction
        """
        self.PortDropDown.clear()
        for port in ports_scan():
            self.PortDropDown.addItem(str(port))

    def close_win(self):
        """
        Exits Application
        Called from the actionExit QAction
        """
        # self.timer.stop()
        self.Plot_2.close()
        self.Plot_1.close()
        self.MainWindow.close()
        from time import sleep
        from sys import exit
        sleep(1)
        exit(0)
        # #  FIGURE OUT BETTER TERMINATION
        # from pyqtgraph import exit as done
        # done()

    def toggle_fft_state(self):
        if self.fft_enable:
            self.fft_enable = False
            self.FFT_button.setStatusTip(
                _translate("Plotting_Gui", "Plot the Fast Fourier Transform of the data.", None))
            self.FFT_button.setText(_translate("Plotting_Gui", "FFT", None))
            self.Plot_1.show()
            self.Plot_2.hide()
        else:
            self.fft_enable = True
            self.FFT_button.setStatusTip(
                _translate("Plotting_Gui", "Return to plotting the time domain signal.", None))
            self.FFT_button.setText(_translate("Plotting_Gui", "Time Domain", None))
            self.Plot_1.hide()
            self.Plot_2.show()

        # Uncheck DualPlot Box if checked
        if self.DualPlot.isChecked():
            self.DualPlot.stateChanged.disconnect(self.dual_plot)
            self.DualPlot.setChecked(False)
            self.DualPlot.stateChanged.connect(self.dual_plot)

    def toggle_plot_state(self):
        if self.open_port:
            self.open_port = False
            self.Plot_Button.setStatusTip(
                _translate("Plotting_Gui", "Start Plotting the selected COM Port\'s data.", None))
            self.Plot_Button.setText(_translate("Plotting_Gui", "Open Port", None))
        else:
            self.open_port = True
            self.Plot_Button.setStatusTip(
                _translate("Plotting_Gui", "Stop Plotting the COM Port\'s data.", None))
            self.Plot_Button.setText(_translate("Plotting_Gui", "Close Port", None))

    def toggle_write_state(self):
        if not self.write_checked:
            self.write_checked = True
            self.Write_Button.setStatusTip(_translate("Plotting_Gui", "Stop Writing incoming data to file", None))
            self.Write_Button.setText(_translate("Plotting_Gui", "Stop Write", None))
        else:
            self.write_checked = False
            self.Write_Button.setStatusTip(_translate("Plotting_Gui", "Start writing data to file.", None))
            self.Write_Button.setText(_translate("Plotting_Gui", "Write", None))

    def file_dup(self):
        from pyqtgraph.Qt.QtGui import QMessageBox
        # noinspection PyCallByClass,PyTypeChecker
        choice = QMessageBox.question(self.MainWindow, 'File Name Error!',
                                      'File(s) Already exists, rename session?',
                                      QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                      QtGui.QMessageBox.Yes)
        if choice == QMessageBox.Yes:
            return True
        else:
            return False

    # @staticmethod
    # def file_dup():
    #     from pyqtgraph.Qt.QtGui import QMessageBox
    #     # noinspection PyCallByClass
    #     choice = QMessageBox.question(None, 'File Name Error!',
    #                                   'File(s) Already exists, rename session?',
    #                                   QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
    #                                   QtGui.QMessageBox.Yes)
    #     if choice == QMessageBox.Yes:
    #         return True
    #     else:
    #         return False

# Conditional check to start for isolated testing
if __name__ == '__main__':
    from templates.Stubs import Parent
    import sys
    app = QtGui.QApplication(sys.argv)
    parent = Parent()
    GUI = GuiHandler(parent)
    sys.exit(app.exec_())
