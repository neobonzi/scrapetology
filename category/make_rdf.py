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

import logging
LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s:%(filename)s:%(lineno)3s:%(levelname)5s:%(funcName)s:%(message)s')
meh = '[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s'
handler.setFormatter(formatter)
LOGGER.addHandler(handler)

SWDB = Namespace("http://starwars.wikia.com/star_wars_ontology.owl#")

#PICKLE_FILE = 'starwars_In-universe_articles.pickle'
#PICKLE_FILE = 'starwars_Category:In-universe_articles.pickle'
def import_ontology(pickle_filename):
    LOGGER.debug('%s', pickle_filename)
    ontology = None
    with open(pickle_filename, 'rb') as file:
        ontology = pickle.load(file)
    LOGGER.debug('DONE')
    return ontology

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

# NOTE: for now instances are subClassOf their parents, this is probably not the best practice and should be changed so that instances are a rdf:type of the class they belong to. However, can't seem to get the code working.
def add_instance(graph, inst_dict, key, class_of):
    title = strip_invalid(inst_dict[key].title)
    href = inst_dict[key].href
    graph_add(graph, URIRef(SWDB[title]), RDF.type, OWL.NamedIndividual)
    # NOTE: line below should be fixed so instances are not subClasses
    graph_add(graph, URIRef(SWDB[title]), RDFS.subClassOf, SWDB[class_of])
    graph_add(graph, URIRef(SWDB[title]), OWL.title, Literal(title))
    graph_add(graph, URIRef(SWDB[title]), OWL.href, Literal(href))

def add_class(graph, sw_dict, key, sw_instances):
    LOGGER.debug('%s', key)
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

def make_rdf(onto):
    # Instantiate the graph
    graph = Graph()

    # Add the ontology
    LOGGER.debug('ADDING:Ontology...')
    graph_add(graph, URIRef('http://example.org/star_wars_ontology.owl'), RDF.type, OWL.Ontology)
    categories = onto.categories
    instances = onto.instances
    for key in categories:
        add_class(graph, categories, key, instances)

    # Bind the OWL and SWDB name spaces
    LOGGER.debug('BINDING:OWL and SWDB name spaces...')
    graph.bind("owl", OWL)
    graph.bind("swdb", SWDB)
    return graph

def main():
    LOGGER.setLevel(logging.INFO)
    # ARGS
    parser = args_make_rdf()
    args = parser.parse_args()

    # SET LOGGING LEVEL
    if args.debug:
        LOGGER.setLevel(logging.DEBUG)
    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)
    if args.quiet:
        LOGGER.disabled = True

    # IMPORT ONTOLOGY
    pickle_filename = args.pickle
    LOGGER.info('Importing Ontology: %s', pickle_filename)
    onto = import_ontology(pickle_filename)

    # BUILD RDF
    LOGGER.info('Building RDF...')
    rdf = make_rdf(onto)

    # SAVE RDF
    output_filename = pickle_filename.rstrip('.pickle') + '.xml'
    LOGGER.info('Saving RDF: %s', output_filename)
    rdf.serialize(output_filename, format='pretty-xml', encoding='utf-8')
    return 0

if __name__ == '__main__':
    sys.exit(main())
