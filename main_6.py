import sys
import random
from PyQt6 import QtWidgets,QtCore,QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog

class Game2048_6x6(QtWidgets.QMainWindow):
    def __init__(self,menu_window=None):
        super().__init__()
        from PyQt6.uic import loadUi
        loadUi("2048_6.ui", self)
        self.grid_size = 6
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.best_score = 0
        self.game_over = False
        self.previous_state = None
        self.menu_window = menu_window
        
        self.setWindowTitle("2048")
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setup_labels()
        print(f"Кнопка меню: {hasattr(self, 'pushButton_2')}")
        self.pushButton.clicked.connect(self.new_game)
        self.pushButton_3.clicked.connect(self.undo_move)
        self.pushButton_2.clicked.connect(self.open_menu)
        
        self.centralwidget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.centralwidget.keyPressEvent = self.keyPressEvent
        
        self.new_game()
        
    def open_menu(self):
     if self.menu_window:
        self.menu_window.show()
        self.hide()

    def setup_labels(self):
        self.cell_labels = [
            [self.lable_00, self.lable_01, self.lable_02, self.lable_03, self.lable_04, self.lable_05],
            [self.lable_10, self.lable_11, self.lable_12, self.lable_13, self.lable_14, self.lable_15],
            [self.lable_20, self.lable_21, self.lable_22, self.lable_23, self.lable_24, self.lable_25],
            [self.lable_30, self.lable_31, self.lable_32, self.lable_33, self.lable_34, self.lable_35],
            [self.lable_40, self.lable_41, self.lable_42, self.lable_43, self.lable_44, self.lable_45],
            [self.lable_50, self.lable_51, self.lable_52, self.lable_53, self.lable_54, self.lable_55]
        ]
 
        for row in self.cell_labels:
            for label in row:
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet(self.get_cell_style(0))
    
    def new_game(self):
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.game_over = False
        self.previous_state = None

        for _ in range(3):
            self.add_random_tile()
        
        self.update_ui()
    
    def undo_move(self):
        if self.previous_state:
            self.board, self.score = self.previous_state
            self.game_over = False
            self.update_ui()
    
    def add_random_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) 
                      for j in range(self.grid_size) if self.board[i][j] == 0]
        
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4
    
    def update_ui(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.board[i][j]
                label = self.cell_labels[i][j]
                label.setText(str(value) if value != 0 else "")
                label.setStyleSheet(self.get_cell_style(value))

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
    
    
    def slide_and_merge(self, line):
        non_zero = [x for x in line if x != 0]
        merged = []
        score_add = 0
        i = 0
        
        while i < len(non_zero):
         if i + 1 < len(non_zero) and non_zero[i] == non_zero[i+1]:
                merged_value = non_zero[i] * 2
                merged.append(merged_value)
                score_add += merged_value
                i += 2 
         else:
                merged.append(non_zero[i])
                i += 1
        
        merged += [0] * (len(line) - len(merged))
        return merged, score_add
    def move_left(self):
        moved = False
        for i in range(self.grid_size):
            row = self.board[i][:]
            new_row, score_add = self.slide_and_merge(row)
            
            if row != new_row:
                moved = True
                self.score += score_add
                self.board[i] = new_row
        return moved

    def move_right(self):
        moved = False
        for i in range(self.grid_size):
            row = self.board[i][::-1]
            new_row, score_add = self.slide_and_merge(row)
            new_row = new_row[::-1] 
            
            if self.board[i] != new_row:
                moved = True
                self.score += score_add
                self.board[i] = new_row
        return moved

    def move_up(self):
        moved = False
        for j in range(self.grid_size):
            column = [self.board[i][j] for i in range(self.grid_size)]
            new_column, score_add = self.slide_and_merge(column)
            
            if column != new_column:
                moved = True
                self.score += score_add
                for i in range(self.grid_size):
                    self.board[i][j] = new_column[i]
        return moved

    def move_down(self):
        moved = False
        for j in range(self.grid_size):
            column = [self.board[i][j] for i in range(self.grid_size)]
            column = column[::-1] 
            new_column, score_add = self.slide_and_merge(column)
            new_column = new_column[::-1] 
            
            original_column = [self.board[i][j] for i in range(self.grid_size)]
            if original_column != new_column:
                moved = True
                self.score += score_add
                for i in range(self.grid_size):
                    self.board[i][j] = new_column[i]
        return moved

    def is_game_over(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.board[i][j] == 0:
                    return False
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if j + 1 < self.grid_size and self.board[i][j] == self.board[i][j+1]:
                    return False
                if i + 1 < self.grid_size and self.board[i][j] == self.board[i+1][j]:
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
    game = Game2048_6x6()
    game.show()
    sys.exit(app.exec())