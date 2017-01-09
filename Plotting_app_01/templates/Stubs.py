# -*- coding: utf-8 -*-
# Stubs.py
"""
Holds objects and classes that serve as blank stubs for testing purposes
creates a dummy QtGui.QApplication to start for testing purposes
"""
import sys
from PyQt4 import QtGui
from multiprocessing import Value


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
        # QtGui.QMainWindow.__init__()

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
        print('Writing...how bout fak you you utter pillak!')
        sys.exit(6)

    @staticmethod
    def update_bit_data():
        print('Bloody Muppet...')
        sys.exit(5)

    @staticmethod
    def begin_plotting():
        print('i tell you where i hid the plot... for a money')
        sys.exit(4)

    @staticmethod
    def open_console():
        print('I\'ll Open you a Console alright ya Cunt!')
        sys.exit(2)

    @staticmethod
    def session_name_update():
        return 'THE SASSY SESSION NAME HERE YA CUNT!!'

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
        return 'UPDATE here you Cheeky Cunt'

    @staticmethod
    def close_app():
        print('Closing App...please hold...\n if nothign is seen in the next few moments...fuckered it up mate...')
        sys.exit(0)
        # noinspection PyUnreachableCode
        print('...now its really fucked good and proper m8... hats off')


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
    app = QtGui.QApplication([])
    test = Parent()
    sys.exit(app.exec_())

else:
    app = QtGui.QApplication([])
    # app.exec_()
