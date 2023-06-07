import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit(self)
        self.text_edit.textChanged.connect(self.scroll_to_bottom)  # 连接文本变化的信号槽

        self.setCentralWidget(self.text_edit)

        self.setWindowTitle("Text Editor")
        self.setGeometry(100, 100, 800, 600)

    def scroll_to_bottom(self):
        scroll_bar = self.text_edit.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())
