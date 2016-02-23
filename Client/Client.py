# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import sys
import json


class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        self.data = ""
        self.jdata = {}
        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.host = host
        self.server_port = server_port
        self.received = ""
        self.out_text = ""
        try:
            # Connect to server and send data
            self.run()
        finally:
            self.disconnect()

        print "Sent:     {}".format(self.data)
        print "Received: {}".format(self.received)



    def run(self):
        print "Type 'help' if stuck"
        while True:
            self.data = raw_input("> ")
            # shit starts here
            i = 0
            if self.data == "help":
                print "HELP\n---------------\nlogin <username> ------ log in with the given username\n" \
                      "logout -------- log out \nmsg <message> ------ send message \nnames ------- list users in chat" \
                      "\nhelp ------- view help text "
                continue
            elif self.data[0:4] == "login":
                # make this a login message
                i = 5
                self.jdata['request'] = "login"
            elif self.data[0:5] == "logout":
                # make this a logout message
                i = 6
                self.jdata['request'] = "logout"
            elif self.data[0:2] == "msg":
                # this is a message
                i = 3
                self.jdata['request'] = "msg"
            elif self.data[0:4] == "names":
                # client asks for names
                i = 5
                self.jdata['request'] = "names"
            # shit ends here (probably not)
            self.jdata['content'] = self.data[i:]       #strip it
            json_data = json.dumps(self.jdata)
            print json.dumps(json_data, indent=4, sort_keys=True)
            self.connection.connect((self.host, self.server_port))
            self.connection.sendall(json_data + "\n")
            self.received = self.connection.recv(1024)


    def disconnect(self):
        # TODO remove itself from connected clients
        self.connection.close()

    def receive_message(self, message):
        # TODO: Handle incoming message
        # print "Received: {}".format(received)
        self.out_text = MessageParser.parse(message)
        print " > " + self.out_text

    def send_payload(self, data):
        # TODO: Handle sending of a payload
        pass

        # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9992)
