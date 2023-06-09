from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        # 设置文本
        self.text_edit.setPlainText("这是一段示例文本。")

        # 创建 QTextCharFormat 对象并设置为红色
        format = QTextCharFormat()
        format.setForeground(QColor("red"))

        # 创建 QTextCursor 对象并将其设置为文本编辑器的光标
        cursor = self.text_edit.textCursor()

        # 将光标移动到文本的中间位置
        cursor.setPosition(6)

        # 将光标向右移动 6 个字符
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, 6)

        # 将选定的文本应用红色格式
        cursor.mergeCharFormat(format)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
