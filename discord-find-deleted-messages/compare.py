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
        for message in data['data'][channel]:
            usr = data['meta']['users'][data['meta']['userindex'][data['data'][channel][message]['u']]]['name']
            ts = datetime.datetime.fromtimestamp(data['data'][channel][message]['t']/1000).strftime('%c')
            messages.append((ts,
                             usr,
                             message, data['data'][channel][message].get('m')))
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
    last_timestamp = max([timestamp for timestamp, _, __, ___ in reference])
    cleaned_ref = set([(timestamp, usr, msg) for timestamp, usr, message, msg in reference if timestamp < last_timestamp])
    cleaned_new = set([(timestamp, usr, msg) for timestamp, usr, message, msg in newest])
    deleted_messages = cleaned_new - cleaned_ref
    print(len(deleted_messages))
    for dmsg in deleted_messages:
        print(dmsg)



def print_data(data):
    for channel in data['meta']['channels']:
        print(channel)
        for message in data['data'][channel]:
            u, t, m = data['data'][channel][message]['u'], data['data'][channel][message]['t'], data['data'][channel][message].get('m')
            # ts = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(t)))
            ts = datetime.datetime.fromtimestamp(t/1000).strftime('%c')
            u = data['meta']['users'][data['meta']['userindex'][u]]
            u = u['name']
            print(f'[{ts}] <{u}>: {m}')


if __name__ == "__main__":
    main(sys.argv[1:])
