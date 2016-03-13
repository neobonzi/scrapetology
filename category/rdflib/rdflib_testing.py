import __future__
# import pickle
# import sys
# sys.path.insert(0, '/mnt/DATA/school/CPE581/scrapetology/category')
# from build_ontology import *
# import pprint
from rdflib import Graph, URIRef, BNode, Namespace, Literal
from rdflib.namespace import RDF, FOAF, RDFS, OWL

test_dict = {
    'category1' : {
        'href' : '/wiki/test_cat_1',
        'title' : 'Test Category 1',
        'parents' : ['None'],
        'children' : ['Category 2'],
        'instances' : ['Instance 1', 'Instance 2']
    },
    'category2' : {
        'href' : '/wiki/test_cat_2',
        'title' : 'Test Category 2',
        'parents' : ['Category 1'],
        'children' : ['Category 3', 'Category 4'],
        'instances' : ['Instance 3', 'Instance 4']
    }
}
#working through category1, issue with DFS?, create the category as an URIRef,
# set the properties of the Node, get to children, for each parent/child need to create new nodes making new Nodes for each.

# RDFlib create a small graph that has class and subclass and instance relationships

#  from the small graph, how do we get relationship information relating sub and super classes together?


def import_pickle_file():
    sw_dump = None
    pickle_file = '/mnt/DATA/school/CPE581/scrapetology/category/starwars_In-universe_articles.pickle'
    with open(pickle_file, 'rb') as pkl_file:
        sw_dump = pickle.load(pkl_file)
        # pprint.pprint(sw_dump)
    return sw_dump

    # iterate through the dictionary
    # get a category
        # create a URIRef for each category
            # URL will need to be http://exmample.org/Category/
            # or http://example.org/Instance/
            # XXX does this matter?

            # if creating nodes as I'm DFSing through the dictionary, how to check if I already have created one?
            # create named nodes for every category in the dictionary.
                #Then create relationships on a second pass through the dictionary
                # do this to avoid see if a URIRef was already created when creating xml/rdf
        # create URIRef for all instances
        # second pass through the categories dictionary
            # for each category we will be creating information/relationship of
                # parent categories
                # child categories / instances
                # Literal(title)
                # Literal(href)
                # graph.add( (subject, predicate, object) )

graph = Graph()

def graph_add(subject, object, predicate):
    global graph
    graph.add((subject, object, predicate))

# def main():
    # for each category in dictionary, create a dictionary that contains category name to URIRef object?
    # for k,v in test_dict:

        # each key is going to be a category
        # 'test_' + k = URIRef('testURI')

def test():
    global graph
    # sw_dump = import_pickle_file()
    # make sure to add new nodes with URIRef
    # bob = URIRef("http://example.org/people/Bob")
    linda = URIRef("http://example.org/people/Linda")
    eve = URIRef("http://example.org/people/Eve")
    ObjectProperty = URIRef('http://example.org/propertyName#')
    # XXX: will likely need a naming convention to determine if vars are Category or Instance, for example. better solution? needed?
        # cat_category_name
        # inst_instance_name

    # name = Literal('Bob') # passing a string
    # age = Literal(24) # passing a python int
    # height = Literal(76.5) # passing a python float

    '''not sure usefulness of this yet'''
    # n = Namespace("http://example.org/people/")
    # n.bob # = rdflib.term.URIRef(u'http://example.org/people/bob')
    # n.eve # = rdflib.term.URIRef(u'http://example.org/people/eve')

    # wrapped the graph.add function
    # graph_add(ObjectProperty, RDFS.subClassOf, URIRef("http://example.org/people/Bob"))
    # graph_add(ObjectProperty, OWL.superClass, eve)
    # graph_add(ObjectProperty, RDF.type, OWL.functional)

    # original syntax
    graph.add( (ObjectProperty, OWL.title, Literal('Title')))
    graph.add( (ObjectProperty, OWL.href, Literal('/wiki/Category')))
    graph.add( (URIRef("http://example.org/people/Bob"), RDF.type, OWL.Person) )
    graph.add( (URIRef("http://example.org/people/Bob"), OWL.name, Literal('Bob')) )
    # graph.add( (bob, OWL.knows, linda) )
    # graph.add( (linda, RDF.type, OWL.Person) )
    # graph.add( (linda, OWL.name, Literal('Linda') ) )
    # graph.add( (linda, OWL.age, Literal(24)) )

    print (graph.serialize(format='xml'))

if __name__ == '__main__':
    # main()
    test()
    # main2()
