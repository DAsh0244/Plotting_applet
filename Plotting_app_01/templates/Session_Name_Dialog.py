# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Session_Name_Dialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(514, 202)
        self.formLayout = QtGui.QFormLayout(Dialog)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.Name_Label = QtGui.QLabel(Dialog)
        self.Name_Label.setObjectName(_fromUtf8("Name_Label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.Name_Label)
        self.Name_Box = QtGui.QLineEdit(Dialog)
        self.Name_Box.setObjectName(_fromUtf8("Name_Box"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.Name_Box)
        self.Text_1 = QtGui.QLabel(Dialog)
        self.Text_1.setScaledContents(False)
        self.Text_1.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.Text_1.setWordWrap(True)
        self.Text_1.setObjectName(_fromUtf8("Text_1"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.Text_1)
        self.Text_2 = QtGui.QLabel(Dialog)
        self.Text_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Text_2.setObjectName(_fromUtf8("Text_2"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.SpanningRole, self.Text_2)
        self.Text_3 = QtGui.QLabel(Dialog)
        self.Text_3.setAlignment(QtCore.Qt.AlignCenter)
        self.Text_3.setObjectName(_fromUtf8("Text_3"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.Text_3)
        self.Text_5 = QtGui.QLabel(Dialog)
        self.Text_5.setAlignment(QtCore.Qt.AlignCenter)
        self.Text_5.setObjectName(_fromUtf8("Text_5"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.SpanningRole, self.Text_5)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.Path_Label = QtGui.QLabel(Dialog)
        self.Path_Label.setObjectName(_fromUtf8("Path_Label"))
        self.horizontalLayout_2.addWidget(self.Path_Label)
        self.Path_Box = QtGui.QLineEdit(Dialog)
        self.Path_Box.setAutoFillBackground(False)
        self.Path_Box.setPlaceholderText(_fromUtf8(""))
        self.Path_Box.setObjectName(_fromUtf8("Path_Box"))
        self.horizontalLayout_2.addWidget(self.Path_Box)
        self.PathButton = QtGui.QToolButton(Dialog)
        self.PathButton.setObjectName(_fromUtf8("PathButton"))
        self.horizontalLayout_2.addWidget(self.PathButton)
        self.formLayout.setLayout(9, QtGui.QFormLayout.SpanningRole, self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout.setWidget(11, QtGui.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.Name_Label.setText(_translate("Dialog", "Session Name:", None))
        self.Text_1.setText(_translate("Dialog", "The Session Name is used to determine what to name files created during this session.", None))
        self.Text_2.setText(_translate("Dialog", "eg: a Session Name of \"First Test\" will produce the following files:", None))
        self.Text_3.setText(_translate("Dialog", "First_Test_X.txt", None))
        self.Text_5.setText(_translate("Dialog", "First_Test_Y.txt", None))
        self.Path_Label.setText(_translate("Dialog", "Session Path:", None))
        self.PathButton.setText(_translate("Dialog", "...", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

