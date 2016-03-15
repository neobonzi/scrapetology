#!/usr/bin/env python3

import pickle
import os
import sys
import logging
LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

from bs4 import BeautifulSoup as bs
import urllib
from urllib import request
import re

import json
from json import JSONEncoder

sys.path.append(os.getcwd())

START_BASE_URL='http://starwars.wikia.com'
START_CAT_URL='wiki/Category:In-universe_articles'
#START_CAT_URL='/wiki/Category:Products_by_company'
#START_CAT_URL='Category:Individuals_by_species'
CAT_ELEMENT_TAG='CategoryTreeLabel CategoryTreeLabelNs14 CategoryTreeLabelCategory'

DELIM='~'
INDENT=4

class WikiParser(object):
    def __init__(self, base_url):
        self.base_url = base_url
    def __str__(self):
        return 'WikiParser'
    def get_page(self, url):
        assert(False)
    def get_category_pages(self, category_url):
        assert(False)

class HTMLWikiParser(WikiParser):
    def __init__(self, base_url):
        self.base_url = base_url
    def __str__(self):
        return 'HTMLWikiParser'
    def get_page(self, url):
        soup = None
        LOGGER.debug('FETCHING:{}'.format(url))
        try:
            read_page = request.urlopen(url)
        except urllib.error.HTTPError as e:
            LOGGER.error('urllib.error.HTTPError:{}'.format(full_url))
            raise e
        soup = bs(read_page, "lxml")
        return soup
    def get_categories(self):
        assert(False)
    def get_instances(self):
        assert(False)

class StarWarsHTMLWikiParser(HTMLWikiParser):
    def __str__(self):
        return 'StarWarsHTMLWikiParser'
    def get_category_pages(self, category_href):
        # GET FIRST PAGE
        LOGGER.debug('CATEGORY:{}'.format(category_href))
        soups = []
        full_url = self.base_url + category_href
        soup = self.get_page(full_url)
        soups.append(soup)
        # 
        re_next_href = '{}.*?{}'.format(category_href,'#mw-subcategories')
        next_tag = soup.findAll('a', href=re.compile(re_next_href))
        while next_tag:
            next_href = None
            # (I'm sorry...)
            for n in next_tag:
                for e in n:
                    if 'next' in e:
                        next_href = n['href']
                        break
                if next_href:
                    break
            if not next_href:
                LOGGER.debug('NEXT:No next tags to follow')
                break
            LOGGER.debug('NEXT:FOLLOWING:{}'.format(n))
            full_url = self.base_url + next_href
            soup = self.get_page(full_url)
            soups.append(soup)
            next_tag = soup.findAll('a', href=re.compile(re_next_href))
        return soups
    def get_categories(self, soups):
        categories = []
        for soup in soups:
            [categories.append(c) for c in soup.findAll('a', class_=CAT_ELEMENT_TAG)]
        [LOGGER.debug('PARSED:CATEGORY:{}'.format(c['href'])) for c in categories]
        return categories
    def get_instances(self, soups):
        instances = []
        for soup in soups:
            mw_pages = soup.findAll("div", id="mw-pages")
            if mw_pages:
                [instances.append(i) for i in mw_pages[0].findAll("a") if i.get('title') and i.get('href')]
        [LOGGER.debug('PARSED:INSTANCE:{}'.format(i.get('href'))) for i in instances]
        return instances;

class Instance(object):
    def __init__(self, base_url, href):
        self.base_url = base_url
        self.href = href
        self.title = Instance.get_title(href)
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
    def __init__(self, base_url, href):
        self.base_url = base_url
        self.href = href
        self.title = Category.get_title(href)
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
        return href.replace('/wiki/','')
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
    def __init__(self, base_url, base_category_url, parser_class):
        self.base = base_url
        self.base_category_url = base_category_url
        self.parser = parser_class(base_url)

        self.base_category = Category.get_title(base_category_url)
        self.name = base_url.replace('http://','').split('.')[0] \
            + '_' + self.base_category.replace('wiki/','')
        self.categories = None
        self.instances = None
        return
    def __str__(self):
        return self.__dict__.__str__()
    def get_json_name(self):
        return '{}.json'.format(self.name)
    def get_pickle_name(self):
        return '{}.pickle'.format(self.name)
    def build_ontology_rec(self, category_url, parent=None, path=''):
        if Ontology.CHILD_LIMIT and Ontology.num_children > Ontology.CHILD_LIMIT:
            LOGGER.debug('EXITING:Child limit of {} reached'.format(CHILD_LIMIT))
            return
        Ontology.num_children += 1

        # PARSE CATEGORY NAME
        title = Category.get_title(category_url)
        path += '/' + title
        category = None

        # CHECK IF SEEN
        seen = title in self.categories
        if seen:
            LOGGER.info('OLD:CATEGORY:{}'.format(path))
            category = self.categories[title]
        else:
            # CREATE NEW CATEGORY
            category = Category(self.base, title)
            self.categories[title] = category
            # PRINT THIS LEVEL
            LOGGER.info('NEW:CATEGORY:{}'.format(path))
        if parent:
            category.add_parent(parent)

        if seen:
            return

        # GRAB AND READ PAGE
        #soup = self.get_category_page(category_url)
        soups = self.parser.get_category_pages(category_url)

        # TRAVERSE CHILDREN
        child_categories = self.parser.get_categories(soups)
        if child_categories:
            for c in child_categories:
                c_href = c['href']
                c_title = Category.get_title(c_href)
                assert(c_href)
                assert(c_title)
                category.add_child(c_title)
                # RECURSE CHILD IF NEW
                if not seen:
                    self.build_ontology_rec(c_href, title, path)
        # GET INSTANCES
        instances = self.parser.get_instances(soups);
        if instances:
            for i in instances:
                i_href = i.get('href')
                i_title = Instance.get_title(i_href)
                assert(i_href)
                assert(i_title)
                instance = None
                seen = i_title in self.instances
                if seen:
                    LOGGER.info('OLD:INSTANCE:{}:{}'.format(path, i_title))
                    instance = self.instances[i_title]
                else:
                    instance = Instance(i_href, i_title)
                    LOGGER.info('NEW:INSTANCE:{}:{}'.format(path, i_title))
                    self.instances[i_title] = instance
                instance.add_parent(title)
                category.add_instance(i_title)
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
        if isinstance(obj, WikiParser):
            return obj.__str__()
        elif isinstance(obj, Instance):
            return obj.__dict__
        elif isinstance(obj, Category):
            return obj.__dict__
        elif isinstance(obj, Ontology):
            return obj.__dict__
        return JSONEncoder.default(self, obj)

def main():
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.info('BUILDING:Star Wars Ontology')
    parser = StarWarsHTMLWikiParser('fuck')
    onto = Ontology(START_BASE_URL, START_CAT_URL, StarWarsHTMLWikiParser)
    json_filename = onto.get_json_name()
    pickle_filename = onto.get_pickle_name()
    cats = onto.get_ontology()
    LOGGER.info(json.dumps(onto, cls=OntologyJSONEncoder, sort_keys=True, indent=4))
    LOGGER.info('Saving {} as {}...'.format('JSON', json_filename))
    with open(json_filename, 'w') as file:
        json.dump(onto, file, cls=OntologyJSONEncoder, sort_keys=True, indent=4)
    LOGGER.info('Pickling {} as {}...'.format('pickle', pickle_filename))
    with open(pickle_filename, 'wb') as file:
        pickle.dump(onto, file)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
