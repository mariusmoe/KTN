# -*- coding: utf-8 -*-
import SocketServer
import json
from datetime import datetime

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""


# CONNECTION_LIST = []
# SOCKET_LIST = []
# RECV_BUFFER = 4096
# PORT = 5000 # ALREADY ASSIGNED
# history = ""


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    global history

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        # TODO json payload from client needs a field for username, it makes it much easier
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        print "new client IP: " + str(self.ip) + " and port: " + str(self.port)

        global history

        self.connection.sendall(history)
        # CONNECTION_LIST.append(self.connection)
        while True:
            data = self.request.recv(1024)

            if not data:
                break

            data = json.loads(data)

            # client has sent a message
            print datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + data['request'] + ': ' + data['content']

            if data['request'] == 'login':
                if self.login(data['content']):
                    self.compose('info', ('successful login by: ' + data['content']))
                else:
                    self.compose('error', 'ERROR during login')
            elif data['request'] == 'logout':
                if self.logout(data['content']):  # not ideal solution
                    self.compose('info', (data['content'] + ' - logged out '))
                else:
                    self.compose('error', 'Ouch, this was embracing. Try telling the system admin that error 9 '
                                          'occured\n'
                                          ' ERROR logout failed')
            elif data['request'] == 'msg':
                self.compose('message', data['content'])
            elif data['request'] == 'names':
                self.compose('info', server.users.keys())

    # extended payload could make it possible to send custom messages to sender (like data['username']) ???

    def send(self, data):
        self.request.send(data)

    def login(self, username):
        """
        log in user

        :rtype: bool
        """
        if username not in server.users:
            server.users[username] = self.request
            return True
        else:
            return False

    def logout(self, username):
        if username in server.users:
            del server.users[username]

    def compose(self, category, data):
        jdata = {}
        jdata['timestamp'] = datetime.now().time()
        jdata['sender'] = 'moe'  # this must be fixed
        jdata['response'] = category
        jdata['content'] = data

        json_data = json.dumps(jdata)
        self.broadcast(json_data)

    def broadcast(self, data):
        for usr in server.users:
            server.users[usr].sendall(data)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """

    def init(self):
        self.history = []
        self.users = {}

    allow_reuse_address = True


if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9992
    print 'moServer running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.init()
    # SOCKET_LIST.append(server)          # add server socket object to the list of readable connections
    server.serve_forever()
