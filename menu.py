import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from main import Game2048
from main_6 import Game2048_6x6

class MenuWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        
        self.last_mode = None  #последний выбранный режим
        self.game_window = None  #запущенное игровое окно
        
        self.setup_button_hover_effects()

        
        self.ui.pushButton_3.clicked.connect(self.close)
        self.ui.pushButton_5.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_6.clicked.connect(self.start_game)
        self.ui.pushButton.clicked.connect(lambda: self.set_game_mod(4))
        self.ui.pushButton_2.clicked.connect(lambda: self.set_game_mod(6))
    
    def start_game(self):
        if self.last_mode is None:
            return 
        if self.game_window is not None:
            self.game_window.close()
            self.game_window = None 
            
        if self.game_window is None:
            if self.last_mode == 4:
                self.game_window = Game2048(menu_window=self)  #создаем экземпляр класса
            elif self.last_mode == 6:
                self.game_window = Game2048_6x6(menu_window=self)  #создаем экземпляр класса
        
        if self.game_window:
            self.game_window.show()
            self.hide()
        
    def set_game_mod(self, mode):
        self.last_mode = mode 
        
    def setup_button_hover_effects(self):
        #список кнопок меню
        menu_buttons = [
            self.ui.pushButton_3,  # Выход
            self.ui.pushButton_4,  # Настройки
            self.ui.pushButton_5,  # Режимы
            self.ui.pushButton_6   # Продолжить
        ]
        
        #применяем эффекты наведения для каждой кнопки
        for button in menu_buttons:
            #сохраняем оригинальный стиль
            original_style = button.styleSheet()
            
            #cоздаем измененный стиль для наведения
            hover_style = original_style.replace(
                "background-color: #d4d4d4;", 
                "background-color: #999;"
            )
            
            # Устанавливаем обработчики событий
            button.enterEvent = lambda event, b=button, s=hover_style: b.setStyleSheet(s)
            button.leaveEvent = lambda event, b=button, s=original_style: b.setStyleSheet(s)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1920, 1080)
        Form.setMinimumSize(QtCore.QSize(1920, 1080))
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 571, 1081))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(parent=self.horizontalLayoutWidget)
        self.widget.setStyleSheet("background-color: #999;\n"
"border-radius: 5px;\n"
"padding: 8px 15px;\n"
"font-weight: bold;")
        self.widget.setObjectName("widget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.widget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 250, 511, 471))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet("background-color: #d4d4d4;\n"
"color: white;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"font-weight: bold;")
        self.pushButton_6.setObjectName("pushButton_6")
        self.verticalLayout_3.addWidget(self.pushButton_6)
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("background-color: #d4d4d4;\n"
"color: white;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"font-weight: bold;")
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout_3.addWidget(self.pushButton_5)
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("background-color: #d4d4d4;\n"
"color: white;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"font-weight: bold;")
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout_3.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: #d4d4d4;\n"
"color: white;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"font-weight: bold;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_3.addWidget(self.pushButton_3)
        self.horizontalLayout.addWidget(self.widget)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(740, 60, 611, 791))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.horizontalLayoutWidget_2)
        self.stackedWidget.setStyleSheet("background-color: #d4d4d4;\n"
"color: white;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"font-weight: bold;")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.page)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(50, 40, 471, 211))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_8 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.horizontalSlider = QtWidgets.QSlider(parent=self.verticalLayoutWidget_3)
        self.horizontalSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_2.addWidget(self.horizontalSlider)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.pushButton = QtWidgets.QPushButton(parent=self.page_2)
        self.pushButton.setGeometry(QtCore.QRect(60, 160, 471, 211))
        self.pushButton.setStyleSheet("background-color: #999;\n"
"border-radius: 5px;\n"
"padding: 8px 15px;\n"
"font-weight: bold;")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.page_2)
        self.pushButton_2.setGeometry(QtCore.QRect(60, 450, 461, 211))
        self.pushButton_2.setStyleSheet("background-color: #999;\n"
"border-radius: 5px;\n"
"padding: 8px 15px;\n"
"font-weight: bold;")
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(parent=self.page_2)
        self.label.setGeometry(QtCore.QRect(230, 380, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(parent=self.page_2)
        self.label_2.setGeometry(QtCore.QRect(230, 670, 101, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_5 = QtWidgets.QLabel(parent=self.page_2)
        self.label_5.setGeometry(QtCore.QRect(260, 180, 261, 171))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_5.setWordWrap(True)
        self.label_5.setOpenExternalLinks(False)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=self.page_2)
        self.label_6.setGeometry(QtCore.QRect(250, 470, 261, 171))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_6.setWordWrap(True)
        self.label_6.setOpenExternalLinks(False)
        self.label_6.setObjectName("label_6")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.page_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 40, 431, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.stackedWidget.addWidget(self.page_2)
        self.horizontalLayout_2.addWidget(self.stackedWidget)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_6.setText(_translate("Form", "Продолжить"))
        self.pushButton_5.setText(_translate("Form", "Режимы"))
        self.pushButton_4.setText(_translate("Form", "Настройки"))
        self.pushButton_3.setText(_translate("Form", "Выход"))
        self.label_8.setText(_translate("Form", "Настройки"))
        self.label_9.setText(_translate("Form", "Громкость эффектов"))
        self.label.setText(_translate("Form", "4 X 4"))
        self.label_2.setText(_translate("Form", "6 X 6"))
        self.label_5.setText(_translate("Form", "Классический вариант игры 2048. Играй в свое удововльствие!"))
        self.label_6.setText(_translate("Form", "Больше поле — больше возможностей"))
        self.label_3.setText(_translate("Form", "Режимы игры"))
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec())
