from flask import render_template, flash, redirect
import rdflib
from rdflib import Graph, URIRef, BNode, Namespace, Literal
from rdflib.namespace import RDF, FOAF, RDFS, OWL
from app import app
from .forms import QueryForm

import logging
LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s:%(filename)s:%(lineno)3s:%(levelname)5s:%(funcName)s:%(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)

import pickle
graph = None
GRAPH_PICKLE_FILENAME='app/static/test.pickle'
LOGGER.debug('LOADING:%s', GRAPH_PICKLE_FILENAME)
with open(GRAPH_PICKLE_FILENAME, 'rb') as file:
    graph = pickle.load(file)
LOGGER.debug('BINDING NAMESPACES')
graph.bind("swdb", Namespace("http://starwars.wikia.com/star_wars_ontology.owl#"))
graph.bind("owl", Namespace("http://www.w3.org/2002/07/owl#"))
LOGGER.debug('LOADING DONE')

@app.route('/')
@app.route('/index')
def index():
    form = QueryForm()
    return render_template('query.html',
                            title='Star Wars Trivia Bot',
                            form=form)

@app.route('/query', methods=['GET', 'POST'])
def query():
    form = QueryForm()
    if form.validate_on_submit():
        LOGGER.debug('QUERY:%s', form.query.data)
        query = form.query.data.replace("What are types of ", "")
        query = query.replace(" ", "_")
        sparql_query = "SELECT ?title WHERE { ?subject rdfs:subClassOf swdb:" + query + " . ?subject owl:title ?title .}"
        LOGGER.debug('QUERY:%s', sparql_query)
        result = graph.query(sparql_query)
        LOGGER.debug('QUERY:%s', 'DONE')
        LOGGER.debug('QUERY:%s', 'PRINTING:results...')
        for row in result:
            item = "%s" % row
            flash(item.replace("_"," "))
        LOGGER.debug('QUERY:%s', 'PRINTING:DONE')
    return redirect('/index')
