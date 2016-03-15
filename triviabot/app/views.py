from flask import render_template, flash, redirect
import rdflib
from rdflib import Graph, URIRef, BNode, Namespace, Literal
from rdflib.namespace import RDF, FOAF, RDFS, OWL
from app import app
from .forms import QueryForm

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
	graph = rdflib.Graph()
	graph.parse('http://jamesbilous.com/static/test.owl')
	graph.bind("swdb", Namespace("http://starwars.wikia.com/star_wars_ontology.owl#"))	
	graph.bind("owl", Namespace("http://www.w3.org/2002/07/owl#"))
	
	query = form.query.data.replace("What are types of ", "")
	query = query.replace(" ", "_")

	result = graph.query("SELECT ?title WHERE { ?subject rdfs:subClassOf swdb:" + query + " . ?subject owl:title ?title .}")
	
	for row in result:
		item = "%s"%row
		flash(item.replace("_"," "))

    return redirect('/index')
