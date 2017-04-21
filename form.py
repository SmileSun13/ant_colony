from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    """Класс, описывающий визуальную часть графического пользовательского интерфейса."""
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1124, 862)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_start = QtWidgets.QPushButton(self.frame_2)
        self.button_start.setObjectName("button_start")
        self.verticalLayout.addWidget(self.button_start)
        self.button_start.setEnabled(False)
        self.label_result = QtWidgets.QLabel(self.frame_2)
        self.label_result.setObjectName("label_result")
        self.verticalLayout.addWidget(self.label_result)
        spacerItem = QtWidgets.QSpacerItem(20, 320, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.button_clear = QtWidgets.QPushButton(self.frame_2)
        self.button_clear.setObjectName("button_clear")
        self.verticalLayout.addWidget(self.button_clear)
        spacerItem1 = QtWidgets.QSpacerItem(20, 320, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.button_export = QtWidgets.QPushButton(self.frame_2)
        self.button_export.setObjectName("button_export")
        self.button_export.setEnabled(False)
        self.verticalLayout.addWidget(self.button_export)
        self.button_import = QtWidgets.QPushButton(self.frame_2)
        self.button_import.setObjectName("button_import")
        self.verticalLayout.addWidget(self.button_import)
        self.horizontalLayout.addWidget(self.frame_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.button_start.setText(_translate("Form", "Старт"))
        self.label_result.setText(_translate("Form", "Здесь будет выведен результат"))
        self.button_clear.setText(_translate("Form", "Очистить поле"))
        self.button_export.setText(_translate("Form", "Экспортировать граф в файл"))
        self.button_import.setText(_translate("Form", "Импортировать граф из файла"))

