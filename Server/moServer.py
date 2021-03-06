# -*- coding: utf-8 -*-
import SocketServer
import json
from time import gmtime, strftime
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

history = []
users = {}

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    global history
    username = ""

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        # TODO json payload from client needs a field for username, it makes it much easier
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.thisusername = ""
        self.valid = False

        print "new client IP: " + str(self.ip) + " : " + str(self.port)

        global history

        # feature to come! history(whoohoo)
        # self.connection.sendall(history)
        # CONNECTION_LIST.append(self.connection)
        while True:
            try:
                # try to read incoming data
                data = self.request.recv(1024)

                if not data:
                    break

                # parse json object
                data = json.loads(data)

                # handle different requests
                if data['request'] == 'login':
                    # print "previously known username: " + self.thisusername + " tied to log in with: " + data['content']
                    if self.login(data['content']):
                        self.thisusername = data['content']
                        self.valid = True
                        self.compose('server', 'message', ('user: ' + data['content'] + " joined this channel!"))
                    else:
                        self.compose('server', 'error', 'ERROR during login')
                        # self.logout('server', 'error', ('user: ' + data['content'] + " name error!"))

                elif data['request'] == 'logout' and self.valid == True:
                    # print "logout requested"
                    if self.logout():  # not ideal solution
                        print "Client with IP: " + str(self.ip) + " : " + str(self.port) + " has logged out successfully"
                        self.valid = False
                        pass    # logic taken over by logout method
                    else:
                        self.compose('server', 'error', 'Ouch, this was embracing. Try telling the system admin that error 9 occured ERROR logout failed')
                elif data['request'] == 'msg' and self.valid == True:
                    history.append(
                                {'username': str(self.thisusername),
                                'timestamp':strftime("%H:%M:%S"),
                                'message':data['content']})
                    self.compose(str(self.thisusername), 'message', data['content'])
                elif data['request'] == 'names' and self.valid == True:
                    self.compose('server', 'info', users.keys())
                elif data['request'] == 'history' and self.valid == True:
                    self.compose('server', 'history', 'The following history:')

                #This elif-statement handles the case of not being a valid user
                elif data['request'] == 'info' or data['request'] == 'history' or data['request'] == 'names' or data['request'] == 'msg' or data['request'] == 'logout' and self.valid == False:
                    print("non-valid username handler ran")
                    self.send('You need to be logged in with a username to use this command')
            except:
                pass
    # extended payload could make it possible to send custom messages to sender (like data['username']) ???

    def send(self, data):
        """
        only send a message back to the sender

        :param data:
        :return: None
        """
        users[self.thisusername].sendall(data)
        #self.request.send(data)
    def login(self, username):
        """
        log in user with the username

        :param username:    the username for the user
        :rtype: bool
        """
        if self.thisusername != "":
            # del users[username]
            # self.logout(username)
            # print "user already logged in"
            return False
        else:
            users[username] = self.request
            return True

    def logout(self):
        """
        log out user

        :param username: user to be logged out
        :return: bool
        """
        # print "username that the server tried to delete: " + self.extrausername
        # del users[self.extrausername]
        # print "tried to delete key: " + self.thisusername
        if self.thisusername in users:
            # users.pop(self.thisusername, None)
            self.compose('server', 'message', ('user: ' + self.thisusername + " left this channel"))
            self.compose('server', 'info', "you are now logged out")
            del users[self.thisusername]
            # self.thisusername = ""
            self.thisusername = ""
            return True
        else:
            return False

    def compose(self, sender, category, data):
        """
        makes the message to be sent ond json encodes it, the message is then handed over to some sort of send() method
        or broadcast() method

        :param sender: who sends the data
        :param category: response type e.g. info, error...
        :param data: param of the response type
        :return: None
        """
        jdata = {}
        jdata['timestamp'] = strftime("%H:%M:%S")
        jdata['sender'] = str(sender)
        jdata['response'] = str(category)
        jdata['content'] = str(data)

        json_data = json.dumps(jdata)

        if category == 'history':
            print "sending history"
            self.send(json_data)
            #print history
            for hist in history:
                jdata['timestamp'] = hist['timestamp']
                jdata['sender'] = hist['username']
                jdata['response'] = 'message'
                jdata['content'] = hist['message']
                json_data = json.dumps(jdata)
                #print json_data
                #print ":((((((((((()))))))))))"
                self.send(json_data)
                time.sleep(0.001)

        elif category == 'error' or category == 'info':
            self.send(json_data)
        else:
            self.broadcast(json_data)

    def broadcast(self, data):
        """
        sends data to all users connected with a username

        :param data:    the json object that is to be sent
        :return: None
        """
        for usr in users:
            users[usr].sendall(data)


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
    HOST, PORT = 'localhost', 9986
    print 'moServer running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
