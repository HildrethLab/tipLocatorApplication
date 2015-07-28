# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tipLocatorUIBase.ui'
#
# Created: Tue Jul 28 13:24:34 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_TipLocator(QtGui.QWidget):
    def setupUi(self, TipLocator):
        TipLocator.setObjectName(_fromUtf8("TipLocator"))
        TipLocator.resize(700, 500)
        TipLocator.setMinimumSize(QtCore.QSize(700, 500))
        TipLocator.setMaximumSize(QtCore.QSize(700, 500))
        self.labelStageControl = QtGui.QLabel(TipLocator)
        self.labelStageControl.setGeometry(QtCore.QRect(130, 100, 91, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelStageControl.setFont(font)
        self.labelStageControl.setObjectName(_fromUtf8("labelStageControl"))
        self.buttonMovementAbort = QtGui.QPushButton(TipLocator)
        self.buttonMovementAbort.setGeometry(QtCore.QRect(270, 140, 71, 71))
        self.buttonMovementAbort.setObjectName(_fromUtf8("buttonMovementAbort"))
        self.entryBoxDirection_Y = QtGui.QLineEdit(TipLocator)
        self.entryBoxDirection_Y.setGeometry(QtCore.QRect(150, 240, 41, 21))
        self.entryBoxDirection_Y.setObjectName(_fromUtf8("entryBoxDirection_Y"))
        self.buttonDirectionNeg_X = QtGui.QPushButton(TipLocator)
        self.buttonDirectionNeg_X.setGeometry(QtCore.QRect(90, 180, 40, 40))
        self.buttonDirectionNeg_X.setMinimumSize(QtCore.QSize(40, 40))
        self.buttonDirectionNeg_X.setMaximumSize(QtCore.QSize(40, 40))
        self.buttonDirectionNeg_X.setObjectName(_fromUtf8("buttonDirectionNeg_X"))
        self.entryBoxDirection_X = QtGui.QLineEdit(TipLocator)
        self.entryBoxDirection_X.setGeometry(QtCore.QRect(90, 240, 41, 21))
        self.entryBoxDirection_X.setObjectName(_fromUtf8("entryBoxDirection_X"))
        self.buttonDirectionPos_Y = QtGui.QPushButton(TipLocator)
        self.buttonDirectionPos_Y.setGeometry(QtCore.QRect(150, 130, 40, 40))
        self.buttonDirectionPos_Y.setMinimumSize(QtCore.QSize(40, 40))
        self.buttonDirectionPos_Y.setMaximumSize(QtCore.QSize(40, 40))
        self.buttonDirectionPos_Y.setObjectName(_fromUtf8("buttonDirectionPos_Y"))
        self.labelMovementDistance = QtGui.QLabel(TipLocator)
        self.labelMovementDistance.setGeometry(QtCore.QRect(20, 242, 60, 21))
        self.labelMovementDistance.setMinimumSize(QtCore.QSize(60, 21))
        self.labelMovementDistance.setMaximumSize(QtCore.QSize(60, 21))
        self.labelMovementDistance.setObjectName(_fromUtf8("labelMovementDistance"))
        self.buttonDirectionPos_X = QtGui.QPushButton(TipLocator)
        self.buttonDirectionPos_X.setGeometry(QtCore.QRect(90, 130, 40, 40))
        self.buttonDirectionPos_X.setMinimumSize(QtCore.QSize(40, 40))
        self.buttonDirectionPos_X.setMaximumSize(QtCore.QSize(40, 40))
        self.buttonDirectionPos_X.setObjectName(_fromUtf8("buttonDirectionPos_X"))
        self.entryBoxDirection_Z = QtGui.QLineEdit(TipLocator)
        self.entryBoxDirection_Z.setGeometry(QtCore.QRect(210, 240, 41, 21))
        self.entryBoxDirection_Z.setObjectName(_fromUtf8("entryBoxDirection_Z"))
        self.buttonDirectionPos_Z = QtGui.QPushButton(TipLocator)
        self.buttonDirectionPos_Z.setGeometry(QtCore.QRect(210, 130, 40, 40))
        self.buttonDirectionPos_Z.setMinimumSize(QtCore.QSize(40, 40))
        self.buttonDirectionPos_Z.setMaximumSize(QtCore.QSize(40, 40))
        self.buttonDirectionPos_Z.setObjectName(_fromUtf8("buttonDirectionPos_Z"))
        self.buttonDirectionNeg_Z = QtGui.QPushButton(TipLocator)
        self.buttonDirectionNeg_Z.setGeometry(QtCore.QRect(210, 180, 40, 40))
        self.buttonDirectionNeg_Z.setMinimumSize(QtCore.QSize(40, 40))
        self.buttonDirectionNeg_Z.setMaximumSize(QtCore.QSize(40, 40))
        self.buttonDirectionNeg_Z.setObjectName(_fromUtf8("buttonDirectionNeg_Z"))
        self.labelMovementDirection = QtGui.QLabel(TipLocator)
        self.labelMovementDirection.setGeometry(QtCore.QRect(20, 170, 60, 21))
        self.labelMovementDirection.setMinimumSize(QtCore.QSize(60, 21))
        self.labelMovementDirection.setMaximumSize(QtCore.QSize(60, 21))
        self.labelMovementDirection.setObjectName(_fromUtf8("labelMovementDirection"))
        self.buttonDirectionNeg_Y = QtGui.QPushButton(TipLocator)
        self.buttonDirectionNeg_Y.setGeometry(QtCore.QRect(150, 180, 40, 40))
        self.buttonDirectionNeg_Y.setMinimumSize(QtCore.QSize(40, 40))
        self.buttonDirectionNeg_Y.setMaximumSize(QtCore.QSize(40, 40))
        self.buttonDirectionNeg_Y.setObjectName(_fromUtf8("buttonDirectionNeg_Y"))
        self.lineTipLocatorStageControl = QtGui.QFrame(TipLocator)
        self.lineTipLocatorStageControl.setGeometry(QtCore.QRect(10, 80, 341, 16))
        self.lineTipLocatorStageControl.setFrameShape(QtGui.QFrame.HLine)
        self.lineTipLocatorStageControl.setFrameShadow(QtGui.QFrame.Sunken)
        self.lineTipLocatorStageControl.setObjectName(_fromUtf8("lineTipLocatorStageControl"))
        self.labelTIpLocator = QtGui.QLabel(TipLocator)
        self.labelTIpLocator.setGeometry(QtCore.QRect(140, 10, 81, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelTIpLocator.setFont(font)
        self.labelTIpLocator.setObjectName(_fromUtf8("labelTIpLocator"))
        self.buttonTipLocatorInitialPositon = QtGui.QPushButton(TipLocator)
        self.buttonTipLocatorInitialPositon.setGeometry(QtCore.QRect(20, 30, 110, 41))
        self.buttonTipLocatorInitialPositon.setObjectName(_fromUtf8("buttonTipLocatorInitialPositon"))
        self.buttonTipLocatorStartRoutine = QtGui.QPushButton(TipLocator)
        self.buttonTipLocatorStartRoutine.setGeometry(QtCore.QRect(130, 30, 110, 41))
        self.buttonTipLocatorStartRoutine.setObjectName(_fromUtf8("buttonTipLocatorStartRoutine"))
        self.buttonTipLocatorAbortRoutine = QtGui.QPushButton(TipLocator)
        self.buttonTipLocatorAbortRoutine.setGeometry(QtCore.QRect(240, 30, 110, 41))
        self.buttonTipLocatorAbortRoutine.setObjectName(_fromUtf8("buttonTipLocatorAbortRoutine"))

        self.retranslateUi(TipLocator)
        QtCore.QMetaObject.connectSlotsByName(TipLocator)

    def retranslateUi(self, TipLocator):
        TipLocator.setWindowTitle(_translate("TipLocator", "Tip Locator", None))
        self.labelStageControl.setText(_translate("TipLocator", "Stage Control", None))
        self.buttonMovementAbort.setText(_translate("TipLocator", "Abort", None))
        self.entryBoxDirection_Y.setText(_translate("TipLocator", "0", None))
        self.buttonDirectionNeg_X.setText(_translate("TipLocator", "-X", None))
        self.entryBoxDirection_X.setText(_translate("TipLocator", "0", None))
        self.buttonDirectionPos_Y.setText(_translate("TipLocator", "+Y", None))
        self.labelMovementDistance.setText(_translate("TipLocator", "Distance:", None))
        self.buttonDirectionPos_X.setText(_translate("TipLocator", "+X", None))
        self.entryBoxDirection_Z.setText(_translate("TipLocator", "0", None))
        self.buttonDirectionPos_Z.setText(_translate("TipLocator", "+Z", None))
        self.buttonDirectionNeg_Z.setText(_translate("TipLocator", "-Z", None))
        self.labelMovementDirection.setText(_translate("TipLocator", "Direction:", None))
        self.buttonDirectionNeg_Y.setText(_translate("TipLocator", "-Y", None))
        self.labelTIpLocator.setText(_translate("TipLocator", "Tip Locator", None))
        self.buttonTipLocatorInitialPositon.setText(_translate("TipLocator", "Initial Position", None))
        self.buttonTipLocatorStartRoutine.setText(_translate("TipLocator", "Start Routine", None))
        self.buttonTipLocatorAbortRoutine.setText(_translate("TipLocator", "Abort Routine", None))

