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

QUERY='SELECT ?title WHERE { ?subject rdfs:subClassOf swdb:Category_Individual . ?subject owl:title ?title .}'

def sparql_query(graph):
    query = QUERY
    LOGGER.debug('QUERY:QUERYING:%s', query)
    results = graph.query(query)
    LOGGER.debug('QUERY:RESULTS :')
    for r in results:
        print(r)
    LOGGER.debug('QUERY:DONE')
def main():
    LOGGER.setLevel(logging.INFO)

    # ARGS
    parser = args_query_rdf()
    args = parser.parse_args()

    # SET LOGGING LEVEL
    if args.debug:
        LOGGER.setLevel(logging.DEBUG)
    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)
    if args.quiet:
        LOGGER.disabled = True

    # IMPORT ONTOLOGY
    graph = None
    graph_pickle_filename = args.pickle
    LOGGER.info('Importing Graph: %s', graph_pickle_filename)
    with open(graph_pickle_filename, 'rb') as file:
        graph = pickle.load(file)
    LOGGER.info('Done Importing')
    sparql_query(graph)
    return 0

if __name__ == '__main__':
    sys.exit(main())
