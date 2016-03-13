#!/usr/bin/env python3

import pickle
import os
import sys
import logging

from bs4 import BeautifulSoup as bs
from urllib import request

import json
from json import JSONEncoder

sys.path.append(os.getcwd())

START_BASE_URL='http://starwars.wikia.com/'
START_CAT_URL='wiki/Category:In-universe_articles'
CAT_ELEMENT_TAG='CategoryTreeLabel CategoryTreeLabelNs14 CategoryTreeLabelCategory'

DELIM='~'
INDENT=4

class Instance(object):
    def __init__(self, href, title):
        self.href = href
        self.title = title
        self.parents = set()
        return
    def __eq__(self, other):
        return self.title.__eq__(other)
    def __hash__(self):
        return self.title.__hash__()
    def __str__(self):
        return self.__dict__.__str__()
    def get_title(href):
        return href.replace('/wiki/','')
    def add_parent(self, parent):
        if parent not in self.parents:
            self.parents.add(parent)
            return True
        else:
            return False

class Category(object):
    def __init__(self, href, title):
        self.href = href
        self.title = title
        self.parents = set()
        self.children = set()
        self.instances = set()
        return
    def __eq__(self, other):
        return self.title.__eq__(other)
    def __hash__(self):
        return self.title.__hash__()
    def __str__(self):
        return self.__dict__.__str__()
    def get_title(href):
        return href.replace('/wiki/','').replace('Category:','')
    def add_parent(self, parent):
        if parent not in self.parents:
            self.parents.add(parent)
            return True
        else:
            return False
    def add_child(self, child):
        if child not in self.children:
            self.children.add(child)
            return True
        else:
            return False
    def add_instance(self, instance):
        if instance not in self.instances:
            self.instances.add(instance)
            return True
        else:
            return False

class Ontology(object):
    CHILD_LIMIT = 0
    num_children = 0
    def __init__(self, base_url, base_category_url):
        self.base = base_url
        self.base_category = Category.get_title(base_category_url)
        self.base_category_url = base_category_url
        self.name = base_url.replace('http://','').split('.')[0] + self.base_category
        self.categories = None
        self.instances = None
        return
    def __str__(self):
        return self.__dict__.__str__()
    def get_json_name(self):
        return '{}.json'.format(self.name)
    def get_pickle_name(self):
        return '{}.pickle'.format(self.name)
    def get_category_page(self, category_url):
        full_url = self.base + category_url
        read_page = request.urlopen(full_url)
        soup = bs(read_page, "lxml")
        return soup
    def get_child_categories(self, soup):
        categories = soup.findAll('a', class_=CAT_ELEMENT_TAG)
        return [c for c in categories if c]
    def get_child_instances(self, soup):
        mw_pages = soup.findAll("div", id="mw-pages")
        if mw_pages:
            instances = mw_pages[0].findAll("a")
            return [i for i in instances if i.get('title') and i.get('href')]
        return None
    def build_ontology_rec(self, category_url, parent=None, path=''):
        if Ontology.CHILD_LIMIT and Ontology.num_children > Ontology.CHILD_LIMIT:
            return
        Ontology.num_children += 1

        # PARSE CATEGORY NAME
        title = Category.get_title(category_url)
        path += '/' + title
        category = None

        # CHECK IF SEEN
        seen = title in self.categories
        if seen:
            print('SEEN:{}'.format(path))
            category = self.categories[title]
        else:
            # CREATE NEW CATEGORY
            category = Category(self.base, title)
            self.categories[title] = category
            # PRINT THIS LEVEL
            print('CAT|' + path)
        if parent:
            category.add_parent(parent)

        if seen:
            return

        # GRAB AND READ PAGE
        soup = self.get_category_page(category_url)

        # TRAVERSE CHILDREN
        children = self.get_child_categories(soup)
        if children:
            for c in children:
                c_href = c['href']
                c_title = Category.get_title(c_href)
                assert(c_href)
                assert(c_title)
                category.add_child(c_title)
                # RECURSE CHILD IF NEW
                if not seen:
                    self.build_ontology_rec(c_href, title, path)
        # GET INSTANCES
        instances = self.get_child_instances(soup);
        if instances:
            for i in instances:
                i_href = i.get('href')
                i_title = i.get('title')
                assert(i_href)
                assert(i_title)
                instance = None
                seen = i_title in self.instances
                if seen:
                    print('SEEN:{}:{}'.format(path, i_title))
                else:
                    instance = Instance(i_href, i_title)
                    print('INS|{}::{}'.format(path, i_title))
                    instance.add_parent(title)
                    category.add_instance(i_title)
                    self.instances[i_title] = instance
        return
    def get_ontology(self):
        if self.categories and self.instances:
            # RETURN ALREADY MADE ONTOLOGY
            return (self.categories, self.instances)

        # BUILD NEW ONTOLOGY
        self.categories = {}
        self.instances = {}
        self.build_ontology_rec(self.base_category_url)
        return (self.categories, self.instances)

class OntologyJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return [x for x in obj]
        elif isinstance(obj, Instance):
            return obj.__dict__
        elif isinstance(obj, Category):
            return obj.__dict__
        elif isinstance(obj, Ontology):
            return obj.__dict__
        return JSONEncoder.default(self, obj)

def main():
    onto = Ontology(START_BASE_URL, START_CAT_URL)
    json_filename = onto.get_json_name()
    pickle_filename = onto.get_pickle_name()
    cats = onto.get_ontology()
    print(json.dumps(onto, cls=OntologyJSONEncoder, sort_keys=True, indent=4))
    print('Saving {} as {}...'.format('JSON', json_filename))
    with open(json_filename, 'w') as file:
        json.dump(onto, file, cls=OntologyJSONEncoder, sort_keys=True, indent=4)
    print('Pickling {} as {}...'.format('pickle', pickle_filename))
    with open(pickle_filename, 'wb') as file:
        pickle.dump(onto, file)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
