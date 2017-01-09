# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BitDepth_Dialog.ui'
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

class BitDepth_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(391, 200)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.Bitdept_label = QtGui.QLabel(Dialog)
        self.Bitdept_label.setObjectName(_fromUtf8("Bitdept_label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.Bitdept_label)
        self.Bitdepth_Label = QtGui.QLabel(Dialog)
        self.Bitdepth_Label.setObjectName(_fromUtf8("Bitdepth_Label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.Bitdepth_Label)
        self.BitDepthDropDown = QtGui.QComboBox(Dialog)
        self.BitDepthDropDown.setEditable(True)
        self.BitDepthDropDown.setObjectName(_fromUtf8("BitDepthDropDown"))
        self.BitDepthDropDown.addItem(_fromUtf8(""))
        self.BitDepthDropDown.addItem(_fromUtf8(""))
        self.BitDepthDropDown.addItem(_fromUtf8(""))
        self.BitDepthDropDown.addItem(_fromUtf8(""))
        self.BitDepthDropDown.addItem(_fromUtf8(""))
        self.BitDepthDropDown.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.BitDepthDropDown)
        self.MSB_LSB_Label = QtGui.QLabel(Dialog)
        self.MSB_LSB_Label.setObjectName(_fromUtf8("MSB_LSB_Label"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.MSB_LSB_Label)
        self.MSB_LSB_Sel = QtGui.QLabel(Dialog)
        self.MSB_LSB_Sel.setObjectName(_fromUtf8("MSB_LSB_Sel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.MSB_LSB_Sel)
        self.MSB_LSBDropDown = QtGui.QComboBox(Dialog)
        self.MSB_LSBDropDown.setObjectName(_fromUtf8("MSB_LSBDropDown"))
        self.MSB_LSBDropDown.addItem(_fromUtf8(""))
        self.MSB_LSBDropDown.addItem(_fromUtf8(""))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.MSB_LSBDropDown)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.SpanningRole, self.label_2)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label)
        self.VoltageRange = QtGui.QComboBox(Dialog)
        self.VoltageRange.setEditable(True)
        self.VoltageRange.setObjectName(_fromUtf8("VoltageRange"))
        self.VoltageRange.addItem(_fromUtf8(""))
        self.VoltageRange.addItem(_fromUtf8(""))
        self.VoltageRange.addItem(_fromUtf8(""))
        self.VoltageRange.addItem(_fromUtf8(""))
        self.VoltageRange.addItem(_fromUtf8(""))
        self.VoltageRange.addItem(_fromUtf8(""))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.VoltageRange)
        self.Dialog_Choice = QtGui.QDialogButtonBox(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Dialog_Choice.sizePolicy().hasHeightForWidth())
        self.Dialog_Choice.setSizePolicy(sizePolicy)
        self.Dialog_Choice.setAutoFillBackground(False)
        self.Dialog_Choice.setOrientation(QtCore.Qt.Horizontal)
        self.Dialog_Choice.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.Dialog_Choice.setCenterButtons(True)
        self.Dialog_Choice.setObjectName(_fromUtf8("Dialog_Choice"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.Dialog_Choice)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.BitDepthDropDown.setCurrentIndex(1)
        QtCore.QObject.connect(self.Dialog_Choice, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.Dialog_Choice, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.Bitdept_label.setText(_translate("Dialog", "Select how many bits your incoming data will be.", None))
        self.Bitdepth_Label.setText(_translate("Dialog", "Bitdepth:", None))
        self.BitDepthDropDown.setStatusTip(_translate("Dialog", " Default is 8 bits.", None))
        self.BitDepthDropDown.setItemText(0, _translate("Dialog", "4", None))
        self.BitDepthDropDown.setItemText(1, _translate("Dialog", "8", None))
        self.BitDepthDropDown.setItemText(2, _translate("Dialog", "10", None))
        self.BitDepthDropDown.setItemText(3, _translate("Dialog", "12", None))
        self.BitDepthDropDown.setItemText(4, _translate("Dialog", "16", None))
        self.BitDepthDropDown.setItemText(5, _translate("Dialog", "24", None))
        self.MSB_LSB_Label.setText(_translate("Dialog", "Select if your packets are MSB or LSB first.", None))
        self.MSB_LSB_Sel.setText(_translate("Dialog", "MSB/LSB first:", None))
        self.MSB_LSBDropDown.setItemText(0, _translate("Dialog", "LSB First", None))
        self.MSB_LSBDropDown.setItemText(1, _translate("Dialog", "MSB First", None))
        self.label_2.setText(_translate("Dialog", "Enter what your signal to your ADC voltage is. Use \'N/A\' if not Applicible", None))
        self.label.setText(_translate("Dialog", "Full Scale Voltage (V):", None))
        self.VoltageRange.setItemText(0, _translate("Dialog", "0 - 3.3", None))
        self.VoltageRange.setItemText(1, _translate("Dialog", "0 - 5", None))
        self.VoltageRange.setItemText(2, _translate("Dialog", "0 - 10", None))
        self.VoltageRange.setItemText(3, _translate("Dialog", "-5 - 5", None))
        self.VoltageRange.setItemText(4, _translate("Dialog", "-2.5 - 2.5", None))
        self.VoltageRange.setItemText(5, _translate("Dialog", "N/A", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = BitDepth_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())