import sys
import random
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QTimer


class Tile(QtWidgets.QLabel):
    def __init__(self, value=0, parent=None):
        super().__init__(parent)
        self.value = value
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_style()
        
    def update_style(self):
        self.setStyleSheet(Tile.get_cell_style(self.value))
        self.setText(str(self.value) if self.value != 0 else "")    
        
    def animate_move(self, new_pos):
        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(100)
        anim.setStartValue(self.geometry())
        anim.setEndValue(QRect(new_pos, self.size()))
        anim.start()
        return anim

        
    @staticmethod
    def get_cell_style(value):
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
        """


class Game2048(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        from PyQt6.uic import loadUi
        loadUi("2048.ui", self)
        self.grid_size = 4
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.best_score = 0
        self.game_over = False
        self.previous_state = None
        self.animation = []
        
        self.setWindowTitle("2048")
        self.setWindowState(Qt.WindowState.WindowFullScreen)
        self.setup_labels()
        
        self.pushButton.clicked.connect(self.new_game)
        self.pushButton_3.clicked.connect(self.undo_move)
        
        self.centralwidget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.centralwidget.keyPressEvent = self.keyPressEvent
        
        self.new_game()
    
    def update_scores(self):
        self.label_2.setText(f"Текущий счет: {self.score}")
        if self.score > self.best_score:
            self.best_score = self.score
        self.label.setText(f"Лучший счет: {self.best_score}")

    def setup_labels(self):
        self.cell_labels = []
        positions = [
            (self.label_4, self.label_3, self.label_5, self.label_6),
            (self.label_7, self.label_10, self.label_11, self.label_12),
            (self.label_8, self.label_13, self.label_14, self.label_15),
            (self.label_9, self.label_16, self.label_17, self.label_18)
        ]
    
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                container = positions[i][j]
                tile = Tile(0, container.parent())
                tile.setGeometry(container.geometry())
                tile.show()
                row.append(tile)
                container.hide() 
            self.cell_labels.append(row)
    
    def new_game(self):
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.game_over = False
        self.previous_state = None

        self.add_random_tile()
        self.add_random_tile()
        self.update_ui()
        
    def wait_for_animations(self, callback):
        if not self.animations:
            callback()
            return

        finished_count = 0
        total = len(self.animations)

        def on_finished():
            nonlocal finished_count
            finished_count += 1
            if finished_count == total:
                callback()

        for anim in self.animations:
         anim.finished.connect(on_finished)
    
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
                tile = self.cell_labels[i][j]
                tile.value = self.board[i][j]
                tile.update_style()
    
        self.update_scores()
        
        if self.is_game_over():
            self.game_over = True
            QtWidgets.QMessageBox.information(self, "Игра окончена", f"Ваш счет: {self.score}")
    
    def apply_animations(self, move_info):
      self.animations = []  # очищаем старые анимации
      for move in move_info:
         if len(move) == 4:
            from_pos, to_pos, line_idx, value = move
            
            if isinstance(from_pos, int):  # вертикально
                from_row, to_row = from_pos, to_pos
                col_idx = line_idx
                tile = self.cell_labels[from_row][col_idx]
                target_rect = self.cell_labels[to_row][col_idx].geometry()
                anim = tile.animate_move(target_rect.topLeft())
                self.animations.append(anim)
            else:  # горизонтально
                from_col, to_col = from_pos, to_pos
                row_idx = line_idx
                tile = self.cell_labels[row_idx][from_col]
                target_rect = self.cell_labels[row_idx][to_col].geometry()
                anim = tile.animate_move(target_rect.topLeft())
                self.animations.append(anim)

    def keyPressEvent(self, event):
        if self.game_over:
            return

        self.previous_state = ([row[:] for row in self.board], self.score)
        
        moved = False
        move_info = []
        
        key = event.key()
        if key == Qt.Key.Key_Up or event.text().lower() in ('w', 'ц'):
            moved, move_info = self.move_up()
        elif key == Qt.Key.Key_Down or event.text().lower() in ('s', 'ы'):
            moved, move_info = self.move_down()
        elif key == Qt.Key.Key_Left or event.text().lower() in ('a', 'ф'):
            moved, move_info = self.move_left()
        elif key == Qt.Key.Key_Right or event.text().lower() in ('d', 'в'):
            moved, move_info = self.move_right()
        else:
            return
            
        if moved:
            self.apply_animations(move_info)
            self.wait_for_animations (lambda:(self.add_random_tile(),self.update_ui))
    def move_up(self):
        move_info = []
        moved = False
        for j in range(self.grid_size):
          column = [self.board[i][j] for i in range(self.grid_size)]
          new_column, score_add, movements = self.slide_and_merge(column, j, True)
          self.score += score_add
          
        
          for i in range(self.grid_size):
            if self.board[i][j] != new_column[i]:
               moved = True
            self.board[i][j] = new_column[i]
          move_info.extend(movements)

        return moved, move_info

    def move_down(self):
     move_info = []
     moved = False
     for j in range(self.grid_size):
        column = [self.board[i][j] for i in range(self.grid_size)]
        new_column, score_add, movements = self.slide_and_merge(column[::-1], j, True)
        new_column = new_column[::-1]
        self.score += score_add
        
        # корректируем позиции для обратного направления
        corrected_movements = []
        grid_size = self.grid_size
        for (from_row, to_row, col_idx, value) in movements:
            new_from_row = grid_size - 1 - from_row
            new_to_row = grid_size - 1 - to_row
            corrected_movements.append((new_from_row, new_to_row, col_idx, value))
        
        move_info.extend(corrected_movements)
        
        for i in range(self.grid_size):
            if self.board[i][j] != new_column[i]:
                moved = True
                self.board[i][j] = new_column[i]
     return moved, move_info

    def move_left(self):
      move_info = []
      moved = False
      for i in range(self.grid_size):        
         row = self.board[i][:]
         new_row, score_add, movements = self.slide_and_merge(row, i, False)
         self.score += score_add
        
         for j in range(self.grid_size):
            if self.board[i][j] != new_row[j]:
                moved = True
                self.board[i][j] = new_row[j]
         move_info.extend(movements)
        
      move_info.extend(movements)
      return moved, move_info

    def move_right(self):
        move_info = []
        moved = False
        for i in range(self.grid_size):
            row = self.board[i][:]
            new_row, score_add, movements = self.slide_and_merge(row[::-1], i, False)
            new_row = new_row[::-1]
            self.score += score_add
            
            # корректируем позиции для обратного направления
            corrected_movements = []
            grid_size = self.grid_size
            for (from_col, to_col, row_idx, value) in movements:
                new_from_col = grid_size - 1 - from_col
                new_to_col = grid_size - 1 - to_col
                corrected_movements.append((new_from_col, new_to_col, row_idx, value))
            
            move_info.extend(corrected_movements)
            
            for j in range(self.grid_size):
                if self.board[i][j] != new_row[j]:
                    moved = True
                    self.board[i][j] = new_row[j]
                    
        return moved, move_info

    def slide_and_merge(self, line, line_idx, is_column):
        non_zero = [x for x in line if x != 0]
        new_line = []
        move_info = []
        score_add = 0
        i = 0
        
        while i < len(non_zero):
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged = non_zero[i] * 2
                new_line.append(merged)
                score_add += merged
                if is_column:
                    move_info.append((line.index(non_zero[i]), len(new_line) - 1, line_idx, non_zero[i]))
                    move_info.append((line.index(non_zero[i + 1]), len(new_line) - 1, line_idx, non_zero[i + 1]))
                else:
                    move_info.append((line.index(non_zero[i]), len(new_line) - 1, line_idx, non_zero[i]))
                    move_info.append((line.index(non_zero[i + 1]), len(new_line) - 1, line_idx, non_zero[i + 1]))
                i += 2
            else:
                new_line.append(non_zero[i])
                original_pos = line.index(non_zero[i])
                new_pos = len(new_line) - 1
                if is_column:
                    move_info.append((original_pos, new_pos, line_idx, non_zero[i]))
                else:
                    move_info.append((original_pos, new_pos, line_idx, non_zero[i]))
                i += 1

        new_line += [0] * (len(line) - len(new_line))
        return new_line, score_add, move_info
    
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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    game = Game2048()
    game.show()
    sys.exit(app.exec())

