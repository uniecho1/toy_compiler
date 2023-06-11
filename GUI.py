import sys
import datetime
from new_new_lexcal import lexer
from syntax import parser
from semantic import semantic_analyzer
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit,  QFileDialog, QWidget, QVBoxLayout, QSplitter, QLabel, QHBoxLayout, QTabWidget
from PySide6.QtGui import QAction, QFont, QTextCursor, QTextCharFormat, QColor
# import PySide6.QtGui.QTextCursor
from PySide6.QtDesigner import QDesignerFormWindowCursorInterface as QDF
# from run import run


class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = None
        self.new_tab_cnt = 0
        self.init_ui()

    def init_ui(self):
        # central_widget = QWidget()
        self.red = False
        self.red_l = 0
        self.red_r = 0
        self.left_title = QLabel("CodeEditor")

        self.left_widget = QTextEdit(self)
        font = QFont()
        font.setPointSize(20)
        self.left_widget.setFont(font)
        self.left_widget.textChanged.connect(self.clear_red)

        self.left_column = QWidget()
        self.left_layout = QVBoxLayout()

        self.left_layout.addWidget(self.left_title)
        self.left_layout.addWidget(self.left_widget)
        self.left_column.setLayout(self.left_layout)

        self.right_title = QLabel("Output")

        self.right_widget = QTextEdit(self)
        self.right_widget.setReadOnly(True)
        font = QFont()
        font.setPointSize(14)
        self.right_widget.setFont(font)

        self.right_column = QWidget()
        self.right_layout = QVBoxLayout()

        self.right_layout.addWidget(self.right_title)
        self.right_layout.addWidget(self.right_widget)
        self.right_column.setLayout(self.right_layout)

        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.left_column, 13)
        self.main_layout.addWidget(self.right_column, 7)
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        self.create_actions()
        self.create_menus()

        self.setWindowTitle("ToyCompiler")
        self.setGeometry(100, 100, 800, 600)

    def clear_red(self):
        if self.red:
            format = QTextCharFormat()
            format.setForeground(QColor("black"))

            cursor = self.left_widget.textCursor()
            cursor.movePosition(QTextCursor.Start)
            cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
            cursor.mergeCharFormat(format)
            self.red = False

    def create_actions(self):
        self.new_action = QAction("New", self, shortcut="Ctrl+N")
        self.new_action.triggered.connect(self.new_file)

        self.open_action = QAction("Open", self, shortcut="Ctrl+O")
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction("Save", self, shortcut="Ctrl+S")
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction("Save AS", self, shortcut="Ctrl+Shift+S")
        self.save_as_action.triggered.connect(self.save_as_file)

        self.exit_action = QAction("Exit", self, shortcut="Ctrl+E")
        self.exit_action.triggered.connect(self.close)

        self.compile_action = QAction(
            "Compile And Run", self, shortcut="Ctrl+Alt+N")
        self.compile_action.triggered.connect(self.compile_and_run)

    def create_menus(self):
        self.menu = self.menuBar()
        self.filemenu = self.menu.addMenu("File")
        self.filemenu.addAction(self.new_action)
        self.filemenu.addAction(self.open_action)
        self.filemenu.addAction(self.save_action)
        self.filemenu.addAction(self.save_as_action)
        self.filemenu.addAction(self.exit_action)
        self.compilemenu = self.menu.addMenu("Compile")
        self.compilemenu.addAction(self.compile_action)

    def update_output(self, info):
        self.right_widget.setText(
            self.right_widget.toPlainText()+info)
        self.right_widget.moveCursor(QTextCursor.MoveOperation.End)

    def to_string(self, token_stream):
        res = ""
        for token in token_stream:
            if token[0] == "dollar":
                continue
            elif token[0] in ['ID', 'NUM']:
                res = res+f"{token[0:2]}"+", "
            else:
                res = res+"[\""+token[0]+"\"]"+", "
        while res[-1] in [" ", ","]:
            res = res[:-1]
        return res

    def move_cursor(self, line, column, l, r):
        self.left_widget.moveCursor(QTextCursor.MoveOperation.Start,
                                    QTextCursor.MoveMode.MoveAnchor)
        for _ in range(line-1):
            self.left_widget.moveCursor(
                QTextCursor.MoveOperation.Down, QTextCursor.MoveMode.MoveAnchor)
        for _ in range(column-1):
            self.left_widget.moveCursor(
                QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.MoveAnchor)

        format = QTextCharFormat()
        format.setForeground(QColor("red"))

        cursor = self.left_widget.textCursor()
        # cursor.movePosition(QTextCursor.Start)
        # cursor.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor, line-1)
        # cursor.movePosition(QTextCursor.Right,
        #                     QTextCursor.KeepAnchor, column-1)
        cursor.setPosition(l)
        cursor.movePosition(QTextCursor.Right,
                            QTextCursor.KeepAnchor, r-l)
        cursor.mergeCharFormat(format)
        self.red = True
        self.red_l = l
        self.red_r = r

    def compile_and_run(self):
        self.save_file()
        instream = self.left_widget.toPlainText()+" dollar"
        time = str(datetime.datetime.now()).split('.')[0]
        self.update_output(f"Compile and Run at {time}:\n\n")
        self.update_output("[LexicalAnalyzing]\n")
        res = lexer(instream).get_token_stream()
        if res[0] == "error":
            res[0] == "LexicalError"
            self.move_cursor(res[1], res[2], res[4], res[5])
            self.update_output(
                f"{res[0]} on line {res[1]}, column {res[2]}: {res[3]}\n\n")
            return
        token_stream, symbol_table = res[1], res[2]
        self.update_output(self.to_string(token_stream)+'\n\n')

        self.update_output("[SyntaxAnalyzing]\n")
        res = parser(token_stream).getparsingtable()
        if res[0] == "error":
            res[0] = "SyntaxError"
            self.move_cursor(res[1], res[2], res[4], res[5])
            self.update_output(
                f"{res[0]} on line {res[1]}, column {res[2]}: {res[3]}\n\n")
            return
        G, node, statement, parsingtree = res[1], res[2], res[3], res[4]
        self.update_output(parsingtree+"\n")

        self.update_output("[Running]\n")
        res = semantic_analyzer(symbol_table, G, node,
                                statement).get_symbol_table()
        if res[0] == "error":
            res[0] = "RuntimeError"
            self.move_cursor(res[1], res[2], res[4], res[5])
            self.update_output(
                f"{res[0]} on line {res[1]}, column {res[2]}: {res[3]}\n\n")
            return
        table = ""
        for id in res[1]:
            val = res[1][id]
            if val != {}:
                table = table+id+" = "+str(val)+"\n"
        self.update_output(table+'\n')
        self.update_output("[Done]\n\n\n")

    def new_file(self):
        self.new_tab_cnt = self.new_tab_cnt+1
        self.add_new_tab("untitled"+str(self.new_tab_cnt))
        new_tab_index = self.left_widget.count()-1
        self.left_widget.setCurrentIndex(new_tab_index)

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open File")
        if file_path:
            self.path = file_path
            with open(file_path, "r") as file:
                self.left_widget.setText(file.read())

    def save_file(self):
        if self.path == None:
            file_dialog = QFileDialog(self)
            file_path, _ = file_dialog.getSaveFileName(self, "Save File")
            self.path = file_path
        else:
            file_path = self.path
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.left_widget.toPlainText())

    def save_as_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Save File", "", "Text Files (*.txt)")
        if file_path:
            self.path = file_path
            with open(file_path, "w") as file:
                file.write(self.left_widget.toPlainText())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = IDE()
    editor.show()
    sys.exit(app.exec())
