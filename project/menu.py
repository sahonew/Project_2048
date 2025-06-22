import sys
import json
import os
from pathlib import Path
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from main import Game2048
from main_6 import Game2048_6x6

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class MenuWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        
        self.last_mode = 4
        self.game_window = None
        self.volume = 50
        self.game_windows = []
        self.setup_menu_buttons()
        self.setup_button_hover_effects()
        self.load_volume_settings()

        self.ui.horizontalSlider.setValue(self.volume)
        self.ui.horizontalSlider.valueChanged.connect(self.set_volume)
        
        self.ui.stackedWidget.setCurrentIndex(0)
        
    def get_settings_path(self):
        if getattr(sys, 'frozen', False):
            return os.path.join(os.path.dirname(sys.executable), "settings.json")
        return "settings.json"

    def get_save_path(self, filename):
            if getattr(sys, 'frozen', False):
                return os.path.join(os.path.dirname(sys.executable), filename)
            return filename

    def setup_menu_buttons(self):
        self.ui.pushButton_3.clicked.connect(self.close)  #выход
        self.ui.pushButton_5.clicked.connect(lambda: self.show_page(1))  #режимы
        self.ui.pushButton_4.clicked.connect(lambda: self.show_page(2))  #настройки
        self.ui.pushButton_8.clicked.connect(lambda: self.show_page(0))  #правила
        self.ui.pushButton_6.clicked.connect(self.start_game)  #играть
        
        self.ui.pushButton.clicked.connect(lambda: self.set_game_mod(4))  #4x4
        self.ui.pushButton_2.clicked.connect(lambda: self.set_game_mod(6))  #6x6
        
        self.ui.pushButton_7.clicked.connect(self.reset_data)

    def show_page(self, page_index):
        self.ui.stackedWidget.setCurrentIndex(page_index)

        
    def set_game_mod(self, mode):
            self.last_mode = mode 
            self.start_game()
            
    def reset_data(self):
        try:
            settings_path = self.get_settings_path()
            save_path_4x4 = self.get_save_path("game_save.json")
            save_path_6x6 = self.get_save_path("game_save6x6.json")

            if os.path.exists(settings_path):
                os.remove(settings_path)
            if os.path.exists(save_path_4x4):
                os.remove(save_path_4x4)
            if os.path.exists(save_path_6x6):
                os.remove(save_path_6x6)
            
            self.volume = 50
            self.ui.horizontalSlider.setValue(self.volume)
            
            for window in self.game_windows:
                if hasattr(window, 'new_game'):
                    window.best_score = 0   
                    window.score = 0      
                    window.has_won = False 
                    window.game_over = False 
                    window.new_game()     
                    window.update_ui()
            
            QtWidgets.QMessageBox.information(self, "Сброс данных", "Все сохраненные данные были удалены")
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось сбросить данные: {str(e)}")
                
    def set_volume(self, value): 
        self.volume = value
        try:
            settings_path = self.get_settings_path()
            with open(settings_path, "w") as f:
                json.dump({"volume": self.volume}, f)
            for window in self.game_windows:
                if hasattr(window, 'update_sound_volume'):
                    window.update_sound_volume()
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
            
    def load_volume_settings(self):
        try:
            settings_path = self.get_settings_path()
            if os.path.exists(settings_path):
                with open(settings_path, "r") as f:
                    settings = json.load(f)
                    self.volume = settings.get("volume", 50)
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")

    def start_game(self):
        if self.game_window is not None:
            if isinstance(self.game_window, (Game2048, Game2048_6x6)):

                self.game_window.save_game_data()
            self.game_window.close()
        if self.last_mode == 4:
            self.game_window = Game2048(menu_window=self)
        elif self.last_mode == 6:
            self.game_window = Game2048_6x6(menu_window=self)
        self.game_windows.append(self.game_window)
        self.game_window.show()
        self.hide()
        
    def setup_button_hover_effects(self):
        menu_buttons = [
            self.ui.pushButton_3,  #выход
            self.ui.pushButton_4,  #настройки
            self.ui.pushButton_5,  #режимы
            self.ui.pushButton_6,  #играть
            self.ui.pushButton_8   #правила
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
            
            #устанавливаем обработчики событий
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
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setStyleSheet("background-color: #d4d4d4;\n"
"color: white;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"font-weight: bold;")
        self.pushButton_8.setObjectName("pushButton_8")
        self.verticalLayout_3.addWidget(self.pushButton_8)
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
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.horizontalLayoutWidget_2.setFont(font)
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.stackedWidget.setFont(font)
        self.stackedWidget.setStyleSheet("background-color: #d4d4d4;\n"
"color: white;\n"
"border-radius: 5px;\n"
"padding: 5px;\n"
"font-weight: bold;")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(parent=self.page_3)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(50, 130, 511, 641))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.verticalLayoutWidget_4.setFont(font)
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_7 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label_7.setWordWrap(True)
        self.label_7.setOpenExternalLinks(False)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(parent=self.page_3)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(50, 40, 509, 78))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_10 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_5)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_5.addWidget(self.label_10)
        self.stackedWidget.addWidget(self.page_3)
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
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.page)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(50, 40, 471, 251))
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
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget_3)
        self.pushButton_7.setStyleSheet("background-color: #999;\n"
"border-radius: 5px;\n"
"padding: 8px 15px;\n"
"font-weight: bold;")
        self.pushButton_7.setObjectName("pushButton_7")
        self.verticalLayout_2.addWidget(self.pushButton_7)
        self.stackedWidget.addWidget(self.page)
        self.horizontalLayout_2.addWidget(self.stackedWidget)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_6.setText(_translate("Form", "Играть"))
        self.pushButton_8.setText(_translate("Form", "Правила"))
        self.pushButton_5.setText(_translate("Form", "Режимы"))
        self.pushButton_4.setText(_translate("Form", "Настройки"))
        self.pushButton_3.setText(_translate("Form", "Выход"))
        self.label_7.setText(_translate("Form", "Цель игры:\n"
"Создать плитку с числом  \"2048\", объединяя одинаковые числа. \n"
"Как играть:\n"
"Игровое поле – это сетка 4×4 или 6×6 .В начале игры появляются две плитка со значением \"2\" или \"4\" в случайных местах и в процессе игры после каждого хода.Используй стрелки (↑, ↓, ←, →) или клавиши клавиатуры (W,A,S,D) чтобы сдвигать все плитки в выбранном направлении.Плитки двигаются до упора, пока не упрутся в край поля или другую плитку.  \n"
"Как складываются плитки:\n"
"Если две одинаковые плитки сталкиваются, ониобъединяются в одну.Например: 2 + 2 = 4, 4 + 4 = 8, и так далее. За один ход плитка может объединиться только один раз.Например, если в ряду стоят \"2\", \"2\", \"2\", то после сдвига получится \"4\",\"2\"\n"
"Как считается счёт:\n"
"Каждый раз, когда две плитки объединяются, их сумма добавляется к твоему счёту. \n"
"Когда ты выиграл или проиграл:\n"
"Если на поле появилась плитка 2048\",ты победил!Можно продолжать играть,чтобы набрать очки,создать новые плитки.Если поле полностью заполнено и нет возможных ходов, игра заканчивается."))
        self.label_10.setText(_translate("Form", "Правила игры"))
        self.label.setText(_translate("Form", "4 X 4"))
        self.label_2.setText(_translate("Form", "6 X 6"))
        self.label_5.setText(_translate("Form", "Классический вариант игры 2048. Играй в свое удововльствие!"))
        self.label_6.setText(_translate("Form", "Больше поле — больше возможностей"))
        self.label_3.setText(_translate("Form", "Режимы игры"))
        self.label_8.setText(_translate("Form", "Настройки"))
        self.label_9.setText(_translate("Form", "Громкость эффектов"))
        self.pushButton_7.setText(_translate("Form", "Сброс данных"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec())
