#!/usr/bin/env python3

import pickle
import os
import sys
import logging

from bs4 import BeautifulSoup as bs
from urllib import request

import json

sys.path.append(os.getcwd())

URL_BASE='http://starwars.wikia.com/'
#CAT_START='wiki/Category:In-universe_articles'
CAT_START='wiki/Category:Artifacts'


def main():
    url_start = URL_BASE + CAT_START
    #print(url_start)
    read_page = request.urlopen(url_start)
    soup = bs(read_page, "lxml")
    nameTags = soup.findAll("div", id="mw-pages")
    for n in nameTags:
        for l in n.findAll("a"):
            title = l.get('title')
            if title:
                print("FUCK '{}'".format(title))
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)

