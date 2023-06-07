import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit,  QFileDialog
from PySide6.QtGui import QAction
from run import run


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

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

        self.exit_action = QAction("Exit", self, shortcut="Ctrl+E")
        self.exit_action.triggered.connect(self.close)

        self.compile_action = QAction("Compile And Run", self, shortcut="F10")
        self.compile_action.triggered.connect(self.compile_and_run)

    def create_menus(self):
        self.menu = self.menuBar()
        self.filemenu = self.menu.addMenu("File")
        self.filemenu.addAction(self.new_action)
        self.filemenu.addAction(self.open_action)
        self.filemenu.addAction(self.save_action)
        self.filemenu.addAction(self.exit_action)
        self.compilemenu = self.menu.addMenu("Compile")
        self.compilemenu.addAction(self.compile_action)

    def compile_and_run(self):
        """
        """
        instream = self.text_edit.toPlainText()
        res = run(instream)
        print(res)

    def new_file(self):
        self.text_edit.clear()

    def open_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Open File")
        if file_path:
            with open(file_path, "r") as file:
                self.text_edit.setText(file.read())

    def save_file(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Save File")
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_edit.toPlainText())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())
