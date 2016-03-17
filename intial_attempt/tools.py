#! /usr/bin/env python3

import pickle
import os
import sys
import logging

import json
from urllib import request

sys.path.append(os.getcwd())
import wikitools

def get_generals_dict(filename='list_generals.txt', log=False):
    generals_dict = {}
    logging.info('Opening {}...'.format(filename))
    with open('list_generals.txt','r') as file:
        for line in file:
            (key, value) = line.replace(',','').replace("'",'').strip().split(':', 1)
            key = key.strip()
            value = value.strip()

            logging.info('Adding {}: {}'.format(key, value))
            generals_dict[key.strip()] = value.strip()
    return generals_dict

def convert_generals(generals, filename='generals.json'):
    assert type(generals) is dict
    with open(filename, 'w') as file:
        json.dump(generals, file, sort_keys=True)
    logging.info('Saved JSON format to {}'.format(filename))

wiki_export_base='https://en.wikipedia.org/wiki/Special:Export/'
def main():
    generals = get_generals_dict()
    convert_generals(generals)
    wikitools.retrieve_xml([a for a in map(lambda x:x.split('/')[-1],generals.values())])
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
