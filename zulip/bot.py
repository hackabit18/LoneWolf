import zulip
import sys
import re
import json
import os

from logic import *

BOT_MAIL = "restaurant-assistant-bot@restaurant-assistant.zulipchat.com"

class ZulipBot(object):
    def __init__(self):
        self.client = zulip.Client(site="https://restaurant-assistant.zulipchat.com/api/")
        self.subscribe_all()
        self.subkeys = ['restaurant-assistant']

    
    def subscribe_all(self):
        print(self.client.get_streams())
        json = self.client.get_streams()["streams"]
        streams = [{"name": stream["name"]} for stream in json]
        self.client.add_subscriptions(streams)

    def process(self, msg):
        message = msg["content"]
        sender_email = msg["sender_email"]
        ttype = msg["type"]
        stream_name = msg['display_recipient']
        stream_topic = msg['subject']

        print(message)

        if sender_email == BOT_MAIL:
            return 

        print("Sucessfully heard.")

        response, intent = get_bot_response(message)
        self.client.send_message({
                    "type": "stream",
                    "subject": msg["subject"],
                    "to": msg["display_recipient"],
                    "content": response
                })

def main():
    bot = ZulipBot()
    bot.client.call_on_each_message(bot.process)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Thanks for using Restaurant Assistant Bot. Bye!")
        sys.exit()