#! /usr/bin/env python3

import json
import sys
import getopt
import datetime

def usage():
    print(
        """Search for deleted messages on multiple discord dump.
        Work with Discord-History-Tracker text dumps: https://github.com/chylex/Discord-History-Tracker
        Usage:
        ./""", sys.argv[0], """dht-reference.txt *dht-newest.txt""")
    exit(2)



def find_latest_timestamp(data):
    pass

def get_messages_id(data):
    messages = []
    for channel in data['meta']['channels']:
        for message_id in data['data'][channel]:
            chan = data['meta']['channels'][channel]['name']
            usr = data['meta']['users'][data['meta']['userindex'][data['data'][channel][message_id]['u']]]['name']
            date = datetime.datetime.fromtimestamp(data['data'][channel][message_id]['t']/1000).strftime('%c')
            ts = data['data'][channel][message_id]['t']/1000
            message = data['data'][channel][message_id].get('m')
            messages.append((chan,
                             ts,
                             date,
                             usr,
                             message_id,
                             message))
    return messages



def get_deleted_messages(data):
    pass

def load_json(file):
    try:
        with open(file) as f:
            return json.load(f)
    except FileNotFoundError:
        print('File ', args[0], " not found.")
        exit()

def print_message(message):
    channel, timestamp, date, usr, message_id, text = message
    print(f'#{channel} | {date} <{usr}> {text}')



def print_data(data):
    for channel in data['meta']['channels']:
        print(channel)
        for message in data['data'][channel]:
            print(f'{channel}:')
            u, t, m = (data['data'][channel][message]['u'],
                       data['data'][channel][message]['t'],
                       data['data'][channel][message].get('m'))

            ts = datetime.datetime.fromtimestamp(t/1000).strftime('%c')
            u = data['meta']['users'][data['meta']['userindex'][u]]
            u = u['name']
            print(f'[{ts}] <{u}>: {m}')

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h")
    except getopt.GetoptError:
        usage()
    if len(opts) or len(args) < 1:
        usage()
    data = load_json(args[0])

    reference = get_messages_id(load_json(args[0]))
    newest = get_messages_id(load_json(args[1]))
    timestamps = [timestamp for _, timestamp, __, ___, ____, ____ in reference]
    last_timestamp = timestamps[-1]
    first_timestamp = timestamps[0]
    last_date = [date for _, timestamp, date, ___, ____, ____ in reference][-1]
    print(f'last timestamp: {last_timestamp} {last_date}')

    cleaned_new = []
    for chan, timestamp, date, usr, message_id, msg in newest:
        if timestamp <= last_timestamp or timestamp > first_timestamp:
            cleaned_new.append((chan, timestamp, date, usr, message_id, msg))


    messages_id = [message_id for chan, timestamp, date, usr, message_id, msg in cleaned_new]
    deleted_messages = []
    for message in reference:
        # print(f'{message}')
        if message[4] not in messages_id:
            print_message(message)
            deleted_messages.append(message)
    print('{} deleted messages'.format(len(deleted_messages)))


if __name__ == "__main__":
    main(sys.argv[1:])
