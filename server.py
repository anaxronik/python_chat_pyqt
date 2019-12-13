from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver


class ServerProtocol(LineOnlyReceiver):
    factory: 'Server'
    login: str = None
    history = []
    number_last_message = 10
    login_list = []

    def lineReceived(self, line):
        try:
            content = line.decode()

            if self.login is not None:
                content = f'Message from {self.login}: {content}'
                for user in self.factory.clients:
                    if user is not self:
                        user.sendLine(content.encode())
                self.history.append(content)
            else:
                if content.startswith('login: '):
                    login_id = content.replace('login: ', '')
                    if login_id not in self.login_list:
                        self.login = login_id
                        self.sendLine('Welcome to chat!'.encode())
                        self.login_list.append(self.login)
                    else:
                        self.sendLine('This login is busy! Please try another.'.encode())

                else:
                    self.sendLine('You must login! login: name'.encode())

        except:
            pass

    def connectionMade(self):
        print('New user connected.')
        self.factory.clients.append(self)
        last_message = self.history[-1 * self.number_last_message:]
        for message in last_message:
            self.sendLine(message.encode())

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)
        print('User disconnect.')
        if self.login in self.login_list:
            self.login_list.remove(self.login)


class Server(ServerFactory):
    protocol = ServerProtocol
    clients: list

    def startFactory(self):
        self.clients = []
        print('Server started')

    def stopFactory(self):
        print('Server stop')


reactor.listenTCP(1234, Server())
reactor.run()
