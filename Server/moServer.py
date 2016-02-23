# -*- coding: utf-8 -*-
import SocketServer
import select
import json

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

CONNECTION_LIST = []
SOCKET_LIST = []
RECV_BUFFER = 4096
# PORT = 5000 # ALREADY ASSIGNED
history = ""


def login(username):
    if username not in CONNECTION_LIST:
        CONNECTION_LIST.append(username)
    else:
        pass

def logout(username):
    if username in CONNECTION_LIST:
        CONNECTION_LIST.remove(username)


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()


def broadcast(server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try:
                socket.send(message)
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    global history

    def setup(self):
        CONNECTION_LIST.append([self.client_address[0], self.client_address[1]])

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # CONNECTION_LIST.append(self.connection)
        while True:
            data = self.request.recv(1024)

            if not data: break

            data = json.loads(data)

            # client has sent a message
            print datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + data['request'] + ': ' + data['content']

            history += data['content'] + ", "

            # Send en melding til klienten om at meldingen ble mottatt

            self.connection.sendall('Message received')



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
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
    SOCKET_LIST.append(server)          # add server socket object to the list of readable connections
    server.serve_forever()





