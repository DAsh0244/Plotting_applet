# -*- coding: utf-8 -*-
# Stubs.py
"""
Holds objects and classes that serve as blank stubs for testing purposes
creates a dummy QtGui.QApplication to start for testing purposes
"""
import sys
from PyQt4 import QtGui
from multiprocessing import Value
app = QtGui.QApplication(sys.argv)


class write_block:
    def __init__(self, val=False):
        self.value = val


class fake_con:
    def __init__(self, value=False):
        self.write_block = write_block(value)


class Parent(object):
    """
    Test Class that has a bunch of stub functions for Main application handler
    """
    def __init__(self):
        super(Parent, self).__init__()
        # QtGui.QMainWindow.__init__()
        self.index = Value('I', 0)
        self.window = QtGui.QMainWindow()

    @staticmethod
    def file_dup():
        choice = QtGui.QMessageBox.question(QtGui.QMessageBox(), 'File Name Error!',
                                            'File(s) Already exists, rename session?',
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                            QtGui.QMessageBox.Yes)
        if choice == QtGui.QMessageBox.Yes:
            return True
        else:
            return False

    @staticmethod
    def disable(obj):
        """
        NEEDED FOR TESTING KILL PROCESSES
        Will Be Removed later
        """
        import sys
        # import time
        print('Disabling Stream!')
        obj.set_stream_enable(False)
        # print(time.time())
        sys.exit(1)

    @staticmethod
    def begin_write():
        print('Writing...')
        sys.exit(6)

    @staticmethod
    def update_bit_data():
        print('updating bit data...')
        sys.exit(5)

    @staticmethod
    def toggle_plotting():
        return 'plotting toggled'

    @staticmethod
    def toggle_write():
        return 'writing toggled'

    @staticmethod
    def update_serial_config():
        return 'serial cfg updated'

    @staticmethod
    def begin_plotting():
        print('plotting started')
        sys.exit(4)

    @staticmethod
    def open_console():
        print('console started...')
        sys.exit(2)

    @staticmethod
    def session_name_update():
        return 'Session name updated'

    @staticmethod
    def update(x, y, z=None, con=fake_con()):
        print(x, y)
        if z is not None:
            a = z
            a += 1
        con.write_block.value = True
        # import time
        # time.sleep(2)
        con.write_block.value = False
        return 'UPDATED screen'

    @staticmethod
    def close_app():
        print('Closing App...')
        sys.exit(0)


class MainWindow(QtGui.QMainWindow):
    def __init__(self, proc_1, proc_2=sys.exit):
        super(MainWindow, self).__init__()
        QtGui.QMainWindow.__init__(self)
        self.toolBar = self.addToolBar("Toolbar")
        # noinspection PyArgumentList
        self.toolBar.addAction(QtGui.QAction('Kill Process', self, triggered=proc_1))
        # noinspection PyArgumentList
        self.toolBar.addAction(QtGui.QAction('Close', self, triggered=proc_2))
        self.show()

if __name__ == '__main__':
    test = Parent()
    test.window.show()
    sys.exit(app.exec_())
