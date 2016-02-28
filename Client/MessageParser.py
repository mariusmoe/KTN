import json


class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history

            # More key:values pairs are needed
        }

    def parse(self, payload):
        # print payload
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            # Response not valid
            print "Response type not valid"

    def parse_error(self, payload):
        # TODO panic !!! there is an error somewhere :o
        # node = payload['response']['stock']['properties']['warehouse']
        # print payload['timestamp'] + " - " + payload['sender'] + " : " + " error: " + payload['content']
        return payload['timestamp'] + " - " + payload['sender'] + " : " + payload['content']

    def parse_info(self, payload):
        # print payload['timestamp'] + " - " + payload['sender'] + " : " + " info: " + payload['content']
        return payload['timestamp'] + " - " + payload['sender'] + " : " + " info: " + payload['content']

    def parse_message(self, payload):
        # print payload['timestamp'] + " - " + payload['sender'] + " : " + payload['content']
        return payload['timestamp'] + " - " + payload['sender'] + " : " + payload['content']

    def parse_history(self, payload):
        # buffer = ""
        # for message in payload['content']:
        return payload['content']
        # Include more methods for handling the different responses...
