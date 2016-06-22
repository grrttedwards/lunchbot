import time
import os
import schedule
import logging

from slackclient import SlackClient

token = os.environ["SLACK_TOKEN"]
lunch_room = "C1JF7S0BB"
test_room = "C1K95FJ12"

where_to_eat = "somewhere"
orders = {}

commands = {
    "help":"I understand the following:\n`help`\n`where <location>`\n`orders`\n`reset`",
    "where":"Looks like we're eating at *;;;;;* today! [not implemented]",
    "orders":"Here's the current list of orders:\n",
    "reset":"Ok, looks like nobody is eating today... :cry:"
}

sc = SlackClient(token)

sc.api_call("channels.join", channel=test_room)
sc.api_call("chat.postMessage", as_user="true", channel=test_room, text="Hi, I'm alive!")

def bot_parse(response):
    reply = ""
    for data in response:

        if "type" not in data.keys() or "text" not in data.keys():
            continue
        if data["type"] == "message":
            msg_text = data["text"]

            if "<@U1K9SPCD7>" in msg_text:
                command = get_command(msg_text)

                if not command:
                    who = who_said(data)
                    reply = "Hey, " + who + " you have to eat _something_..."
                    sc.api_call("chat.postMessage", as_user="true", channel=test_room, text=reply)
                    continue

                keyword = command.split()[0]

                if keyword in commands.keys():
                    reply = commands[keyword]

                if keyword == "help":
                    reply = "Hi I'm lunchbot. I reset every morning.\n" + reply
                elif keyword == "where":
                    reply = reply.replace(";;;;;", where_to_eat)
                elif keyword == "orders":
                    if len(orders) == 0:
                        reply = "There are no orders today!"
                    else:
                        for who in orders.keys():
                            reply += who + ": *" + orders[who] + "*" + "\n"
                elif keyword == "reset":
                    orders.clear()
                else:
                    who = who_said(data)
                    lunch = command
                    reply = "Hi, " + who + ". Putting you down for: *" + lunch + "*"
                    who = who.replace("@","")
                    orders[who] = lunch

                sc.api_call("chat.postMessage", as_user="true", channel=test_room, text=reply)


def get_command(msg):
    breakdown = msg.split()
    lunch = ""
    for i in range(len(breakdown)):
        if "<@U1K9SPCD7>" in breakdown[i]:
            lunch = breakdown[i+1:]

    return " ".join(lunch).replace("@lunchbot", "")


def who_said(response):
    users = sc.api_call("users.list")
    for user in users["members"]:
        if response["user"] == user["id"]:
            return "@" + user["name"]
    return "Mystery Person"


def reset_job():
    orders.clear()
    logging.info("cleared orders at 8:00 utc")


def main():

    schedule.every().day.at("8:00").do(reset_job)

    if sc.rtm_connect():
        while True:
            response = sc.rtm_read()
            if response:
                logging.info(response)
                bot_parse(response)
            schedule.run_pending()
            time.sleep(1)
    else:
        logging.error("Connection Failed")


if __name__ == "__main__":
    main()
    
