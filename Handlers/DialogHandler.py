# -*- coding: utf-8 -*-
"""Handlers for Dialog Popup Boxes"""
# Copyright 2016 : Danyal Ahsanullah
from PyQt4 import QtGui
from templates.BitDepth_Dialog import BitDepth_Dialog
from templates.Session_Name_Dialog import Ui_Dialog

""" Logging setup: """
import logging
from os import getcwd
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # CRITICAL , ERROR , WARNING , INFO , DEBUG , NOTSET
FH = logging.FileHandler('{}\\Debug\\debug.log'.format(getcwd()))
FMT = logging.Formatter("%(asctime)s - %(name)s - %(message)s")
FH.setFormatter(FMT)
logger.addHandler(FH)


class StartSessionDialog(QtGui.QDialog, Ui_Dialog):
    """ Handler for Session Dialog """
    def __init__(self, cfg):
        super(StartSessionDialog, self).__init__()
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        name, path = cfg.get_session_data()
        self.Name_Box.setText(name)
        self.Path_Box.setText(path)
        self.PathButton.clicked.connect(self.file_pick)
        self.show()

    def file_pick(self):
        """ Handles the QToolButton to browse File System to select save location """
        old_path = self.Path_Box.text()
        # logger.debug('old path: "{}"'.format(old_path))
        # noinspection PyTypeChecker,PyCallByClass
        save_path = QtGui.QFileDialog.getExistingDirectory(self, 'Save Location')
        # logger.debug('selected path: "{}"'.format(save_path))
        if save_path == '':
            self.Path_Box.setText(old_path)
            return old_path
        else:
            self.Path_Box.setText(save_path)
            return save_path

    def get_session_values(self):
        """ Returns Values from Session Dialog Box """
        from datetime import datetime as dt
        today = dt.now().strftime("%d-%b-%Y--%H-%M-%f")
        # logging.info('Current Time: {}'.format(today))
        res = self.exec_()
        if res == self.Accepted:
            if self.Name_Box.text():  # returns 0 if empty
                # logger.info(self.Name_Box.text())
                return self.Name_Box.text(), self.Path_Box.text()
            else:
                return today, self.Path_Box.text()
        elif res == self.Rejected:
            # logger.info('No text Entered')
            return today, self.Path_Box.text()


class StartBitDepthDialog(QtGui.QDialog, BitDepth_Dialog):
    """ Dialog Box to Get User Set ADC Bit Depth, MSB/LSB first, Voltage Range, packet size"""
    def __init__(self, cfg):
        super(StartBitDepthDialog, self).__init__()
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        bit_max = self.BitDepthDropDown.count() - 1
        packet_max = self.PacketDropDown.count() - 1
        bit_validator = QtGui.QIntValidator(1, int(self.BitDepthDropDown.itemText(bit_max)), self)
        packet_validator = QtGui.QIntValidator(1, int(self.PacketDropDown.itemText(packet_max)), self)
        self.BitDepthDropDown.setValidator(bit_validator)
        self.PacketDropDown.setValidator(packet_validator)
        self.BitDepthDropDown.setCurrentIndex(cfg.bit_layout[0])
        self.MSB_LSBDropDown.setCurrentIndex(cfg.bit_layout[1])
        # ' - '.join(cfg.Config.MaxVoltage, cfg.Config.MaxVoltage)
        self.VoltageRange.setCurrentIndex(cfg.bit_layout[2])
        self.PacketDropDown.setCurrentIndex(cfg.bit_layout[3])
        self.show()
        del bit_max, packet_max

    def get_bit_values(self):
        """
        Returns Values from bit depth dialog box in the order:
        ( ( BitDepth<int> , MSB/LSB<str> , Voltage_rage<str>), Layout<QArray> ,
          ( BitDepthIndex<int>, MSB/LSBIndex<int>, VoltageIndex<int>) )
        """
        vals = (int(self.BitDepthDropDown.currentText()), self.MSB_LSBDropDown.currentText().split(' ')[0],
                self.VoltageRange.currentText().strip())
        layout = (self.BitDepthDropDown.currentIndex(), self.MSB_LSBDropDown.currentIndex(),
                  self.VoltageRange.currentIndex())
        res = self.exec_()
        if res == self.Accepted:
            vals = (int(self.BitDepthDropDown.currentText()), self.MSB_LSBDropDown.currentText().split(' ')[0],
                    self.VoltageRange.currentText().strip(' '), int(self.PacketDropDown.currentText()))
            layout = (self.BitDepthDropDown.currentIndex(), self.MSB_LSBDropDown.currentIndex(),
                      self.VoltageRange.currentIndex(), self.PacketDropDown.currentIndex())
            # logger.info(vals)
            # print(vals + layout)
        # else:
            # logger.info(vals)
            # logger.info('BitDepth Cancelled')
        # return information about current box state for later reconstructions of box
        return vals, layout

# Conditional check to start
if __name__ == '__main__':
    import sys
    from templates.ConfigOptions import ConfigData
    import os
    # logger.info(os.getcwd())
    app = QtGui.QApplication(sys.argv)
    window = QtGui.QMainWindow()
    window.Config = ConfigData()
    window.Config.set_session_data(name_path=('Logging_App_name', os.getcwd()))
    window.toolBar = window.addToolBar("Toolbar")
    # noinspection PyArgumentList
    window.toolBar.addAction(QtGui.QAction('Session', window,
        triggered=lambda: window.Config.set_session_data(
            name_path=(StartSessionDialog(window.Config).get_session_values(), os.getcwd()))))
    # noinspection PyArgumentList
    window.toolBar.addAction(QtGui.QAction('Bit', window,
        triggered=lambda: window.Config.set_bit_data(StartBitDepthDialog(window.Config).get_bit_values())))

    window.show()

    sys.exit(app.exec_())
