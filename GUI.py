import sys
import datetime
from lexical import lexer
from syntax import parser
from semantic import semantic_analyzer
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit,  QFileDialog, QWidget, QVBoxLayout, QSplitter
from PySide6.QtGui import QAction, QFont, QTextCursor
# from run import run


class IDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = None
        self.init_ui()

    def init_ui(self):
        # central_widget = QWidget()

        layout = QSplitter(self)
        self.setCentralWidget(layout)

        font = QFont()

        font.setPointSize(20)
        self.text_edit = QTextEdit(self)
        # self.text_edit.setDocumentTitle("fuck")
        self.text_edit.setFont(font)
        layout.addWidget(self.text_edit)
        # self.setCentralWidget(self.text_edit)

        font.setPointSize(14)
        self.output_info = QTextEdit(self)
        self.output_info.setFont(font)
        self.output_info.setReadOnly(True)
        # self.output_info.textChanged.connect(self.scroll_to_bottom)
        layout.addWidget(self.output_info)

        layout.setSizes([500, 200])

        self.create_actions()
        self.create_menus()

        self.setWindowTitle("ToyCompiler")
        self.setGeometry(100, 100, 800, 600)

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

    # def scroll_to_bottom(self):
    #     cursor = self.output_info.textCursor()
    #     self.output_info.moveCursor(QTextCursor.MoveOperation.End)
    #     scroll_bar = self.output_info.verticalScrollBar()
    #     scroll_bar.setValue(scroll_bar.maximum())

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
        self.output_info.setText(
            self.output_info.toPlainText()+info)
        self.output_info.moveCursor(QTextCursor.MoveOperation.End)

    def to_string(self, token_stream):
        res = ""
        for token in token_stream:
            if token[0] in ['ID', 'NUM']:
                res = res+f"{token[0:2]}"+", "
            else:
                res = res+"[\""+token[0]+"\"]"+", "
        while res[-1] in [" ", ","]:
            res = res[:-1]
        return res

    def compile_and_run(self):
        """
        """
        self.save_file()
        instream = self.text_edit.toPlainText()
        time = str(datetime.datetime.now()).split('.')[0]
        self.update_output(f"Compile and Run at {time}:\n\n")
        self.update_output("[LexicalAnalyzing]\n")
        res = lexer(instream).gettokens()
        if res[0] == "error":
            res[0] == "LexicalError"
            self.update_output(
                f"{res[0]} on line {res[1]}, column {res[2]}: {res[3]}\n\n")
            return
        token_stream, symbol_table = res[1], res[2]
        self.update_output(self.to_string(token_stream)+'\n\n')

        self.update_output("[SyntaxAnalyzing]\n")
        res = parser(token_stream).getparsingtable()
        if res[0] == "error":
            res[0] = "SyntaxError"
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
        self.text_edit.clear()

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open File")
        if file_path:
            self.path = file_path
            with open(file_path, "r") as file:
                self.text_edit.setText(file.read())

    def save_file(self):
        if self.path == None:
            file_dialog = QFileDialog(self)
            file_path, _ = file_dialog.getSaveFileName(self, "Save File")
            self.path = file_path
        else:
            file_path = self.path
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_edit.toPlainText())

    def save_as_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Save File", "", "Text Files (*.txt)")
        if file_path:
            self.path = file_path
            with open(file_path, "w") as file:
                file.write(self.text_edit.toPlainText())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = IDE()
    editor.show()
    sys.exit(app.exec())
