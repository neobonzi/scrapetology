#!/usr/bin/env python3

from rdflib import Graph, URIRef, BNode, Namespace, Literal
from rdflib.namespace import RDF, FOAF, RDFS, OWL
from build_ontology import *
from args import *
from itertools import islice
import pickle
import pprint
import sys
import re

SWDB = Namespace("http://starwars.wikia.com/star_wars_ontology.owl#")

def import_pickle_file():
    sw_dump = None
    pickle_file = 'starwars_In-universe_articles.pickle'
    with open(pickle_file, 'rb') as pkl_file:
        sw_dump = pickle.load(pkl_file)
    return sw_dump

def graph_add(graph, subject, object, predicate):
    try:
        graph.add((subject, object, predicate))
    except:
        pass

def strip_invalid(text):
    ir = re.sub(r'\s', '_', text)
    ir2 = ir.replace("\"", "")
    ir3 = ir2.replace("'", "")
    ir4 = ir3.replace("^", "")
    return ir4

def add_instance(graph, inst_dict, key, class_of):
    title = strip_invalid(inst_dict[key].title)
    href = inst_dict[key].href
    graph_add(graph, URIRef(SWDB[title]), RDF.type, OWL.NamedIndividual)
    graph_add(graph, URIRef(SWDB[title]), RDFS.subClassOf, SWDB[class_of])
    graph_add(graph, URIRef(SWDB[title]), OWL.title, Literal(title))
    graph_add(graph, URIRef(SWDB[title]), OWL.href, Literal(href))

def add_class(graph, sw_dict, key, sw_instances):
    title = strip_invalid(sw_dict[key].title)
    href = sw_dict[key].href
    parents = sw_dict[key].parents
    instances = sw_dict[key].instances
    graph_add(graph, URIRef(SWDB[title]), RDF.type, OWL.Class)
    graph_add(graph, URIRef(SWDB[title]), OWL.title, Literal(title))
    graph_add(graph, URIRef(SWDB[title]), OWL.href, Literal(href))

    # parent should be the title, can use to look up self.categories[title]
    if parents:
        for parent in parents:
            parent = strip_invalid(parent)
            graph_add(graph, URIRef(SWDB[title]), RDFS.subClassOf, URIRef(SWDB[parent]))
    if instances:
        for instance in instances:
            add_instance(graph, sw_instances, instance, title)

def sparql_query(graph):
    qres = graph.query(
        '''SELECT ?subject
           WHERE {
              ?subject rdfs:subClassOf* swdb:category2
           }''')

    for row in qres:
        print(row)

def print_slice(graph, sw_categories, key, sw_instances):
    # DEBUG - take a small slice of the dicitonary for testing
    n_items = islice(sw_categories.keys(), 0, 10)
    for key in n_items:
        add_class(graph, sw_categories, key, sw_instances)

def print_graph(graph_filename):
    # DEBUG - print the data for testing
    with open(graph_filename) as file:
        for line in file:
            print(line, end='')
        
def build_graph(args):
    graph = Graph()
    sw_ontology = import_pickle_file()
    sw_categories = sw_ontology.categories
    sw_instances = sw_ontology.instances

    # add the ontology
    graph_add(graph, URIRef('http://example.org/star_wars_ontology.owl'), RDF.type, OWL.Ontology)

    # iterate through dictionary and build graph
    for key in sw_categories.keys():
        add_class(graph, sw_categories, key, sw_instances)

    # Bind the OWL and SWDB name spaces
    graph.bind("owl", OWL)
    graph.bind("swdb", SWDB)

    # get filename from user or use default
    graph_filename = None
    if args:
        graph_filename = args.filename[0]
    else:
        graph_filename = 'star_wars_ontology.xml'

    # write the data to disk
    graph.serialize(graph_filename, format='pretty-xml', encoding='utf-8')

def main():
    parser = args_build_graph()
    args = parser.parse_args()
    build_graph(args)

if __name__ == '__main__':
    main()
