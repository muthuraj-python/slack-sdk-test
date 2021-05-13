
import os
from datetime import datetime

from prettytable import PrettyTable
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token="xoxp-2068454142305-2052760857829-2062051938148-841f691df83436c342af3b7bb3c079cc")

def print_messages(messages):
    t = PrettyTable(['Sender', 'Message', 'DateTime'])
    for i in messages:
        t.add_row([i['user'], i['text'], datetime.fromtimestamp(float(i['ts'])).isoformat()])
        # print(i['user'], i['text'], datetime.fromtimestamp(float(i['ts'])).isoformat(), "\n")
    print(t)
    print("\n")

def filter_messages(data, from_date_time_timestamp, to_date_time_timestamp):

    messages = [i for i in data['messages'] if from_date_time_timestamp <= int(i['ts'].split('.')[0]) <= to_date_time_timestamp]
    print_messages(messages)
    return messages

def main(from_date_time=None, to_date_time=None):

    try:
        # response = client.chat_postMessage(channel='#test', text="Hello world!") // to send message to 'test' channel
        response = client.conversations_history(channel='C021JNCS56Z')
        if from_date_time and to_date_time:
            from_date_time_timestamp = datetime.fromisoformat(from_date_time)
            to_date_time_timestamp = datetime.fromisoformat(to_date_time)
            return filter_messages(response.data, datetime.timestamp(from_date_time_timestamp), datetime.timestamp(to_date_time_timestamp))
        print_messages(response.data['messages'])
        return response.data
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error: {e.response['error']}")


if __name__ == '__main__':

    
    from_date_time = '2021-05-11 00:00:00'
    to_date_time = '2021-05-11 23:59:59'

    #Partial Data
    print("+------Messages from {} - to {} -----+\n".format(from_date_time, to_date_time))
    main(from_date_time, to_date_time)

    print("+------All Messages-----+\n")
    #All data
    main()

    
