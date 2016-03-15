# import __future__
import pickle
import sys
sys.path.insert(0, '/mnt/DATA/school/CPE581/scrapetology/category')
from build_ontology import *
import pprint
from rdflib import Graph, URIRef, BNode, Namespace, Literal
from rdflib.namespace import RDF, FOAF, RDFS, OWL
from itertools import islice
import re

SWDB = Namespace("http://starwars.wikia.com/star_wars_ontology.owl#")

def import_pickle_file():
    sw_dump = None
    pickle_file = '/mnt/DATA/school/CPE581/scrapetology/category/starwars_In-universe_articles.pickle'
    with open(pickle_file, 'rb') as pkl_file:
        sw_dump = pickle.load(pkl_file)
        # pprint.pprint(sw_dump)
    return sw_dump

def graph_add(graph, subject, object, predicate):
    graph.add((subject, object, predicate))

def strip_invalid(text):
    ir = re.sub(r'\s', '_', text)
    ir2 = ir.replace("\"", "")
    ir3 = ir2.replace("'", "")
    ir4 = ir3.replace("^", "")
    # print ('trimmed to: ', ir4)
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

def build_graph():
    graph = Graph()
    sw_ontology = import_pickle_file()
    sw_categories = sw_ontology.categories
    sw_instances = sw_ontology.instances

    # add the ontology
    graph_add(graph, URIRef('http://example.org/star_wars_ontology.owl'), RDF.type, OWL.Ontology)

    # DEBUG - take a small slice of the dicitonary for testing
    # n_items = islice(sw_categories.keys(), 0, 10)
    # for key in n_items:
    #     add_class(graph, sw_categories, key, sw_instances)

    # iterate through dictionary and build graph
    for key in sw_categories.keys():
        add_class(graph, sw_categories, key, sw_instances)

    # Bind the OWL and SWDB name spaces
    graph.bind("owl", OWL)
    graph.bind("swdb", SWDB)

    # write the data to disk
    graph_filename = 'test.xml'
    graph.serialize(graph_filename, format='pretty-xml', encoding='utf-8')

    # DEBUG - print the data for testing
    # with open(graph_filename) as file:
    #     for line in file:
    #         print(line, end='')

if __name__ == '__main__':
    build_graph()
