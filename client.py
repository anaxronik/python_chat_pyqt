from PyQt5 import QtWidgets
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver
import sys

from design import Ui_MainWindow


class ConnectorProtocol(LineOnlyReceiver):
    factory: 'Connector'

    def connectionMade(self):
        self.factory.window.protocol = self
        self.factory.window.plainTextEdit.appendPlainText('Connection to server.')

    def lineReceived(self, line):
        self.factory.window.plainTextEdit.appendPlainText(line.decode())


class Connector(ClientFactory):
    protocol = ConnectorProtocol
    window: 'ChatWindow'

    def __init__(self, window: 'ChatWindow') -> None:
        super().__init__()
        self.window = window


class ChatWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    reactor = None
    protocol: 'ConnectorProtocol'

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_handlers()

    def init_handlers(self):
        self.pushButton.clicked.connect(self.send_message)

    def closeEvent(self, *args, **kwargs):
        self.reactor.callFromThread(self.reactor.stop)

    def send_message(self):
        message = self.lineEdit.text()
        self.plainTextEdit.appendPlainText(message)
        self.protocol.sendLine(message.encode())
        self.lineEdit.clear()


app = QtWidgets.QApplication(sys.argv)

import qt5reactor

window = ChatWindow()
window.show()

qt5reactor.install()

from twisted.internet import reactor

reactor.connectTCP('localhost',
                   1234,
                   Connector(window))

window.reactor = reactor
reactor.run()
