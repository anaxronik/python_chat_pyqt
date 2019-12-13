import sys
from PyQt5 import QtWidgets
from design import Ui_MainWindow


class ChatWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def send_message(self):
        message = self.lineEdit.text()
        self.plainTextEdit.appendPlainText(message)
        self.lineEdit.clear()



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ChatWindow()
    window.show()  # Отображает окно
    app.exec_()  # Заставляет окно ожидать и не дает ему закрыться сразу после инициализации.


if __name__ == '__main__':
    main()
