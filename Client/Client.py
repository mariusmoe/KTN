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
        """
        try:
            # Connect to server and send data
            self.run()
        finally:
            self.disconnect()
        """
        self.run()          # trengs denne å kalles??
        print "Sent:     {}".format(self.data)
        print "Received: {}".format(self.received)



    def run(self):
        print "Type 'help' if stuck"
        self.connection.connect((self.host, self.server_port))
        thread1 = MessageReceiver(self, self.connection)
        thread1.start()
        while True:
            self.data = raw_input(">>> ")
            print "\033[A                             \033[A"
            # shit starts here
            # print self.data
            i = 0
            if self.data == "help":
                print "HELP\n---------------\n\nlogin <username> ------ log in with the given username\n" \
                      "logout -------- log out \nmsg <message> ------ send message \nnames ------- list users in chat" \
                      "\nhelp ------- view help text "
                continue
            elif self.data[:5] == "login":
                # make this a login message
                i = 6
                self.jdata['request'] = "login"
            elif self.data[:6] == "logout":
                # make this a logout message
                i = 7
                self.jdata['request'] = "logout"
            elif self.data[:3] == "msg":
                # this is a message
                i = 4
                self.jdata['request'] = "msg"
            elif self.data[:5] == "names":
                # client asks for names
                i = 6
                self.jdata['request'] = "names"
            else:
                print "ERROR - no command was recognised"
                continue
            # shit ends here (probably not)
            self.jdata['content'] = self.data[i:]       #strip it
            json_data = json.dumps(self.jdata)
            # print "JSON to be sent: " + json_data
            # print json.dumps(json_data, indent=4, sort_keys=True)

            self.connection.sendall(json_data) # + "\n")
            # self.received = self.connection.recv(1024)        # v2
            # print self.received
        self.disconnect()


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
    client = Client('localhost', 9986)
