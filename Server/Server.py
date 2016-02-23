# -*- coding: utf-8 -*-
import SocketServer
import select

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

CONNECTION_LIST = {}
RECV_BUFFER = 4096
# PORT = 5000 # ALREADY ASSIGNED
"""
server_socket = server_socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0",  PORT))
server_socket.listen(10)

CONNECTION_LIST.append(server_socket)
print "Chat server start on port " + str(PORT)

while True:
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
    for sock in read_sockets:
        #new connection
        if sock == server_socket:
            #handels case where there is a new connectionrecived through server_socket
            sockfd, addr = server_socket.accept()
            CONNECTION_LIST.append(sockfd)
            print "Client (%s, %s) connected" % addr

            broadcast_data(sockfd, "[%s:%s] entered room\n" % addr")
        #incomming message
        else:
            try:
                data = sock.recv(RECV_BUFFER)
                if data:
                    broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)

            except:
                broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                print "Client (%s, %s) is offline" % addr
                sock.close()
                CONNECTION_LIST.remove(sock)
                continue

server_socket.close()
"""

def broadcast_data(sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(data)
            except:
                socket.close()
                CONNECTION_LIST.remove(socket)


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        self.data = self.connection.recv(1024).strip()
        print "{} wrote:".format(self.ip)
        print self.data
        CONNECTION_LIST[str(self.ip) + ":" + str(self.port)] = 1 # THIS SOULD BE THE USERNAME???
        print CONNECTION_LIST
        if self.data == "exit":
            raise Exception
        self.request.sendall(self.data.upper())
        # Loop that listens for messages from the client
        while True:
            # received_string = self.connection.recv(4096)
            # received_string = self.connection.recv(1024)

            # TODO: Add handling of received payload from client
            # self.request is the TCP socket connected to the client
            pass


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
    HOST, PORT = 'localhost', 9994
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
