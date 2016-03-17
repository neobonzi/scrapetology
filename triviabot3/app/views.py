from flask import render_template, flash, redirect
import rdflib
from rdflib import Graph, URIRef, BNode, Namespace, Literal
from rdflib.namespace import RDF, FOAF, RDFS, OWL
from app import app
from .forms import QueryForm

import os
import sys
sys.path.append(os.getcwd())
from query_parser import *

import logging
LOGGER = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s:%(filename)s:%(lineno)3s:%(levelname)5s:%(funcName)s:%(message)s')
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
LOGGER.setLevel(logging.DEBUG)

import pickle
graph = None
GRAPH_PICKLE_FILENAME='app/static/sw_graph.pickle'
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
    query_parser = ImmediateChildrenParser()
    form = QueryForm()
    if form.validate_on_submit():
        input = form.query.data.replace("What are types of ", "")

        # Parse Query
        LOGGER.debug('QUERY:INPUT:%s', input)
        sparql_query = query_parser.get_query(input)
        LOGGER.debug('QUERY:SPARQL:%s', sparql_query)

        # Results
        results = None
        try:
            LOGGER.debug('QUERY:%s', 'RUNNING')
            results = graph.query(sparql_query)
            LOGGER.debug('QUERY:%s', 'DONE')
            LOGGER.debug('QUERY:%s', 'PRINTING:results...')
            # Print Results
            print_results(input, results, query_parser)
            LOGGER.debug('QUERY:%s', 'PRINTING:DONE')
        except Exception as e:
            # Ignore Exceptions
            flash('"{}" resulted in an error: {}'.format(input, e))
            LOGGER.error('CAUGHT:%s', e)
            pass

    LOGGER.debug('RETURNING')
    return redirect('/index')

def print_results(input, results, parser):
    if not results:
        info_str = 'Alas, no results for "{}".'.format(input)
        flash(info_str)
        flash("Here's the resulting query:")
        flash(parser.get_query(input))
        return
    info_str = 'Results for "{}"'.format(input)
    flash(info_str)
    flash('-' * len(info_str))
    format = lambda x : parser.unformat_entity('%s' % x)
    sorted_results = [format(r) for r in results]
    sorted_results.sort()
    for row in sorted_results:
        #item = "%s" % row
        #item = parser.unformat_entity(item)
        flash(row)
    return

@app.route('/immediate_parents', methods=['GET', 'POST'])
def immediate_parents():
    query_parser = ImmediateParentsParser()
    form = QueryForm()
    if form.validate_on_submit():
        input = form.query.data

        # Parse Query
        LOGGER.debug('QUERY:INPUT:%s', input)
        sparql_query = query_parser.get_query(input)
        LOGGER.debug('QUERY:SPARQL:%s', sparql_query)

        # Results
        results = None
        try:
            LOGGER.debug('QUERY:%s', 'RUNNING')
            results = graph.query(sparql_query)
            LOGGER.debug('QUERY:%s', 'DONE')
            LOGGER.debug('QUERY:%s', 'PRINTING:results...')
            # Print Results
            print_results(input, results, query_parser)
            LOGGER.debug('QUERY:%s', 'PRINTING:DONE')
        except Exception as e:
            # Ignore Exceptions
            flash('"{}" resulted in an error: {}'.format(input, e))
            LOGGER.error('CAUGHT:%s', e)
            pass
    LOGGER.debug('RETURNING')
    return render_template('immediate_parents.html',
            title='Star Wars Trivia Bot:Immediate Parents',
                            form=form)

@app.route('/immediate_children', methods=['GET', 'POST'])
def immediate_children():
    query_parser = ImmediateChildrenParser()
    form = QueryForm()
    if form.validate_on_submit():
        input = form.query.data

        # Parse Query
        LOGGER.debug('QUERY:INPUT:%s', input)
        sparql_query = query_parser.get_query(input)
        LOGGER.debug('QUERY:SPARQL:%s', sparql_query)

        # Results
        results = None
        try:
            LOGGER.debug('QUERY:%s', 'RUNNING')
            results = graph.query(sparql_query)
            LOGGER.debug('QUERY:%s', 'DONE')
            LOGGER.debug('QUERY:%s', 'PRINTING:results...')
            # Print Results
            print_results(input, results, query_parser)
            LOGGER.debug('QUERY:%s', 'PRINTING:DONE')
        except Exception as e:
            # Ignore Exceptions
            flash('"{}" resulted in an error: {}'.format(input, e))
            LOGGER.error('CAUGHT:%s', e)
            pass

    LOGGER.debug('RETURNING')
    #return redirect('/index')
    return render_template('immediate_children.html',
            title='Star Wars Trivia Bot:Immediate Parents',
                            form=form)
@app.route('/all_parents', methods=['GET', 'POST'])
def all_parents():
    query_parser = AllParentsParser()
    form = QueryForm()
    if form.validate_on_submit():
        input = form.query.data

        # Parse Query
        LOGGER.debug('QUERY:INPUT:%s', input)
        sparql_query = query_parser.get_query(input)
        LOGGER.debug('QUERY:SPARQL:%s', sparql_query)

        # Results
        results = None
        try:
            LOGGER.debug('QUERY:%s', 'RUNNING')
            results = graph.query(sparql_query)
            LOGGER.debug('QUERY:%s', 'DONE')
            LOGGER.debug('QUERY:%s', 'PRINTING:results...')
            # Print Results
            print_results(input, results, query_parser)
            LOGGER.debug('QUERY:%s', 'PRINTING:DONE')
        except Exception as e:
            # Ignore Exceptions
            flash('"{}" resulted in an error: {}'.format(input, e))
            LOGGER.error('CAUGHT:%s', e)
            pass

    LOGGER.debug('RETURNING')
    #return redirect('/index')
    return render_template('all_parents.html',
            title='Star Wars Trivia Bot:Immediate Parents',
                            form=form)

@app.route('/all_children', methods=['GET', 'POST'])
def all_children():
    query_parser = AllChildrenParser()
    form = QueryForm()
    if form.validate_on_submit():
        input = form.query.data

        # Parse Query
        LOGGER.debug('QUERY:INPUT:%s', input)
        sparql_query = query_parser.get_query(input)
        LOGGER.debug('QUERY:SPARQL:%s', sparql_query)

        # Results
        results = None
        try:
            LOGGER.debug('QUERY:%s', 'RUNNING')
            results = graph.query(sparql_query)
            LOGGER.debug('QUERY:%s', 'DONE')
            LOGGER.debug('QUERY:%s', 'PRINTING:results...')
            # Print Results
            print_results(input, results, query_parser)
            LOGGER.debug('QUERY:%s', 'PRINTING:DONE')
        except Exception as e:
            # Ignore Exceptions
            flash('"{}" resulted in an error: {}'.format(input, e))
            LOGGER.error('CAUGHT:%s', e)
            pass

    LOGGER.debug('RETURNING')
    #return redirect('/index')
    return render_template('all_children.html',
            title='Star Wars Trivia Bot:Immediate Parents',
                            form=form)

@app.route('/sparql', methods=['GET', 'POST'])
def sparql():
    query_parser = WikiOutputParser()
    form = QueryForm()
    if form.validate_on_submit():
        input = form.query.data

        # Parse Query
        LOGGER.debug('QUERY:INPUT:%s', input)
        sparql_query = query_parser.get_query(input)
        LOGGER.debug('QUERY:SPARQL:%s', sparql_query)

        # Results
        results = None
        try:
            LOGGER.debug('QUERY:%s', 'RUNNING')
            results = graph.query(sparql_query)
            LOGGER.debug('QUERY:%s', 'DONE')
            LOGGER.debug('QUERY:%s', 'PRINTING:results...')
            # Print Results
            print_results(input, results, query_parser)
            LOGGER.debug('QUERY:%s', 'PRINTING:DONE')
        except Exception as e:
            # Ignore Exceptions
            flash('"{}" resulted in an error: {}'.format(input, e))
            LOGGER.error('CAUGHT:%s', e)
            pass

    LOGGER.debug('RETURNING')
    #return redirect('/index')
    return render_template('sparql.html',
            title='Star Wars Trivia Bot:Immediate Parents',
                            form=form)
