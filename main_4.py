import sys
import random
from PyQt6 import QtWidgets,QtCore,QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class Game2048(QtWidgets.QMainWindow):
    def __init__(self,menu_window=None):
        super().__init__()
        from PyQt6.uic import loadUi
        loadUi("2048.ui", self)
        self.grid_size = 4 #размер игрового поля 4х4
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)] #инициализация двумеронного списка(матрицы) размером игрового поля self.grid_size который заполнен нулями
        self.score = 0 #текущий счет
        self.best_score = 0  #текущий счет
        self.game_over = False #флаг окончании игры
        self.previous_state = None #переменная хранит предыдущее состояние поля
        self.menu_window = menu_window
        
        self.setWindowTitle("2048")
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setup_labels() #настройка лейблов
        self.pushButton.clicked.connect(self.new_game)
        self.pushButton_3.clicked.connect(self.undo_move) #присвоевание кнпокам функции
        self.pushButton_2.clicked.connect(self.open_menu)  # Кнопка для открытия меню
        
        self.centralwidget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.centralwidget.keyPressEvent = self.keyPressEvent #настройка клавиатруры и обработки нажатия клавиш
        
        self.new_game() #запуск новой игры

    def open_menu(self):
     if self.menu_window:
        self.menu_window.show()
        self.hide()
            
    def setup_labels(self):
        self.cell_labels = [
            self.label_4, self.label_3, self.label_5, self.label_6,
            self.label_7, self.label_10, self.label_11, self.label_12,
            self.label_8, self.label_13, self.label_14, self.label_15,
            self.label_9, self.label_16, self.label_17, self.label_18
        ] #все плитки собираются в список

        for label in self.cell_labels:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet(self.get_cell_style(0)) #для каждого лейбл а в списке добовлеться стиль
    
    def new_game(self):
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.game_over = False
        self.previous_state = None #сброс игрового поля,очищение матрицы,нулевое значение счета,установление окончание игры и сброс сохраненного состояния игры

        self.add_random_tile()
        self.add_random_tile()#создание новых плиток 
        
        self.update_ui()#обновление интерфейса
    
    def undo_move(self): #отмена прошлого хода
        
        if self.previous_state: #проверка существет ли переменная
            self.board, self.score = self.previous_state #устанволение состоянии матрицы и счета как в предыдцщес состоянии 
            self.game_over = False #сброс фложка окончания игры 
            
            self.update_ui() #обновлние игры
    
    def add_random_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) 
                      for j in range(self.grid_size) if self.board[i][j] == 0]  #запоминает координаты пустых клеток
        
        if empty_cells:
            i, j = random.choice(empty_cells) #выбирает случайную пару и в зависимости от вероятности заполняет ее числом
            self.board[i][j] = 2 if random.random() < 0.9 else 4
    
    def update_ui(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.board[i][j]  #установка текущего значении в соотвестви с значением в матрице 
                label = self.cell_labels[i * self.grid_size + j]  #присваивает ячейке списки соотвествущий лейбл 
                label.setText(str(value) if value != 0 else "")  #выводит тект лейблу в соотвесвтии с значением
                label.setStyleSheet(self.get_cell_style(value))  # устанавливает цвет и стиль плитки в соответствии с её значением
                
        self.label_2.setText(f"Текущий счет: {self.score}")
        if self.score > self.best_score:
            self.best_score = self.score
        self.label.setText(f"Лучший счет: {self.best_score}")
        
        
        if self.is_game_over() and not self.game_over:
            self.game_over = True
            dialog = GameOverDialog(self.score, self)
            dialog.exec()
            
    def get_cell_style(self, value):
        colors = {
            0: "#c7c7c7",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }
        
        font_size = 40 if value < 100 else 30 if value < 1000 else 20
        text_color = "#776e65" if value < 8 else "#f9f6f2"
        
        return f"""
            background-color: {colors.get(value, "#3c3a32")};
            color: {text_color};
            font-weight: bold;
            border-radius: 5px;
            font-size: {font_size}px;
            qproperty-alignment: AlignCenter;
        """
    
    def keyPressEvent(self, event):
        if self.game_over:
            return
        
        self.previous_state = ([row[:] for row in self.board], self.score)
        
        moved = False
        key_text = event.text().lower()
        key_code = event.key()
        if key_code == Qt.Key.Key_Up or key_text in ('w','ц'):
            moved = self.move_up()
        elif key_code == Qt.Key.Key_Down or key_text in ('s','ы'):
            moved = self.move_down()
        elif key_code == Qt.Key.Key_Left or key_text in ('a','ф'):
            moved = self.move_left()
        elif key_code == Qt.Key.Key_Right or key_text in ('d','в'):
            moved = self.move_right()
        else:
            return
        
        if moved:
            self.add_random_tile()
            self.update_ui() 
    
    def move_up(self):
        moved = False
        for j in range(self.grid_size):
            column = [self.board[i][j] for i in range(self.grid_size)]
            new_column, score_add = self.slide_and_merge(column)
            self.score += score_add
            
            for i in range(self.grid_size):
                if self.board[i][j] != new_column[i]:
                    moved = True
                    self.board[i][j] = new_column[i]
        return moved
    
    def move_down(self):
        moved = False
        for j in range(self.grid_size):
            column = [self.board[i][j] for i in range(self.grid_size)]
            new_column, score_add = self.slide_and_merge(column[::-1])
            new_column = new_column[::-1]
            self.score += score_add
            
            for i in range(self.grid_size):
                if self.board[i][j] != new_column[i]:
                    moved = True
                    self.board[i][j] = new_column[i]
        return moved
    
    def move_left(self):
        moved = False
        for i in range(self.grid_size):
            row = self.board[i][:]
            new_row, score_add = self.slide_and_merge(row)
            self.score += score_add
            
            for j in range(self.grid_size):
                if self.board[i][j] != new_row[j]:
                    moved = True
                    self.board[i][j] = new_row[j]
        return moved
    
    def move_right(self):
        moved = False
        for i in range(self.grid_size):
            row = self.board[i][:]
            new_row, score_add = self.slide_and_merge(row[::-1])
            new_row = new_row[::-1]
            self.score += score_add
            
            for j in range(self.grid_size):
                if self.board[i][j] != new_row[j]:
                    moved = True
                    self.board[i][j] = new_row[j]
        return moved
    
    def slide_and_merge(self, line):
        non_zero = [x for x in line if x != 0]
        new_line = []
        score_add = 0
        i = 0
        
        while i < len(non_zero):
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged = non_zero[i] * 2
                new_line.append(merged)
                score_add += merged
                i += 2
            else:
                new_line.append(non_zero[i])
                i += 1
        
        new_line += [0] * (len(line) - len(new_line))
        return new_line, score_add
    
    def is_game_over(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    return False

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                current = self.board[i][j]
                if j + 1 < self.grid_size and self.board[i][j + 1] == current:
                    return False
                if i + 1 < self.grid_size and self.board[i + 1][j] == current:
                    return False
        
        return True
    
class GameOverDialog(QDialog):
    def __init__(self, score, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setupUi(self)
        self.score = score
        self.setWindowTitle("Игра окончена")
        self.setFixedSize(400, 300)
        self.label_3.setText(f"СЧЕТ: {self.score}")
        self.pushButton.clicked.connect(self.accept)
        self.pushButton.clicked.connect(self.close)
        self.setStyleSheet("""
            QDialog {
                background: transparent;
            }
            QLabel {
                font-weight: bold;
            }
        """)
        screen_geometry = QtWidgets.QApplication.primaryScreen().availableGeometry()
        center_point = screen_geometry.center()
        self.move(center_point - self.rect().center())

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.widget = QtWidgets.QWidget(parent=Dialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 400, 400))
        self.widget.setStyleSheet("background-color: #e8e8e8;\n"
"border-radius: 10px;")
        self.widget.setObjectName("widget")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 361, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #FF5733;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: #999;")
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.pushButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.pushButton.setStyleSheet("background-color: #999;\n"
"color: white;\n"
"border-radius: 5px;\n"
"padding: 8px 15px;\n"
"font-weight: bold;\n"
"")
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "ИГРА ОКОНЧЕНА"))
        self.label_3.setText(_translate("Dialog", "СЧЕТ:"))
        self.pushButton.setText(_translate("Dialog", "OK"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    game = Game2048()
    game.show()
    sys.exit(app.exec())