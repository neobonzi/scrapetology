#!/usr/bin/env python3

from rdflib import Graph, URIRef, BNode, Namespace, Literal
from rdflib.namespace import RDF, FOAF, RDFS, OWL
from build_ontology import *
from args import *
from itertools import islice
import json
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

MW='mw-pages'
def check_ontology(onto):
    assert(onto)
    ontoInstancesToRemove = set()
    for cat in onto.categories:
        category = onto.categories[cat]
        categoryInstancesToRemove = set()
        for i in category.instances:
            if MW in i:
                instance = onto.instances[i]
                LOGGER.error('FOUND:%s', json.dumps(instance, cls=OntologyJSONEncoder, sort_keys=True, indent=4))
                categoryInstancesToRemove.add(i)
                ontoInstancesToRemove.add(i)
        for i in categoryInstancesToRemove:
            LOGGER.error('REMOVING:%s:%s', cat, i)
            category.instances.remove(i)
    for i in ontoInstancesToRemove:
        LOGGER.error('REMOVING:ONTOLOGY:%s', i)
        del onto.instances[i]
    return


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
    onto = None
    onto_pickle_filename = args.pickle
    LOGGER.info('Importing Ontology: %s', onto_pickle_filename)
    with open(onto_pickle_filename, 'rb') as file:
        onto = pickle.load(file)
    LOGGER.info('CHECKING Ontology...')
    check_ontology(onto)
    LOGGER.info('CHECKING Ontology...')
    check_ontology(onto)
    LOGGER.info('DONE')
    with open(onto_pickle_filename, 'wb') as file:
        pickle.dump(onto, file)
    return 0

if __name__ == '__main__':
    sys.exit(main())
