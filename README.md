# Towards Automatic Ontology Building
CPE-581

Winter 2016

## Team Members:
* James Bilous
* Jon Doughty
* Jeff McGovern

## Project Description:
Scrapetology is a web application with tools written in python to allow
for the gathering of data, restructuring of data into an ontology, and querying of the
data via web interface. The ontology is ultimately hosted on a website which allows

Using the web interface:

The Scrapetology web interface was created using Flask and can be hosted on any server
technology such as Nginx and Apache. The web interface consists of a simple form
that can be provided with natural language questions in the forms enumerated below.

The views.py file in the swpedia folder must be modified so it points to a hosted
ontology either online or on a local machine. There is an example provided for
the starwars dbpedia at http://jamesbilous.com/static/test.owl.

Currently, queries in the following forms are allowed
	"What are instances of X" - where X is a class field that exists as a "subclassOf"
	property of a triple in the scraped ontology. Underscores can be omitted in favor of spaces.

Further features have been added in the triviabot3/ version:

* Finding immediate child/parent category and instance relationships
* Finding all child/parent category and instance relationships
* Limited SPARQL querying, with examples for unions and intersections for easy copying and modification

## Description of Relevant Files:

* category/
  * Contains code to parse a MediaWiki's Category page hierarchy via html and code to convert the resulting data structure into an RDF/OWL representation.
* triviabot/
  * A python2 implementation of the Star Wars Trivia Bot located at:
    * http://jamesbilous.com/
* triviabot3/
  * A python3 implementation of the Star Wars Trivia Bot, with a different URL and pages added as thus:
    * http://jdmcg.org:5000/
    * http://jdmcg.org:5000/immediate_parents
    * http://jdmcg.org:5000/immediate_children
    * http://jdmcg.org:5000/all_parents
    * http://jdmcg.org:5000/all_children
    * http://jdmcg.org:5000/sparql
* LOG.md
  * The log of hours for each teammate
* README.md
  * This document, describing the project and the relevant files.
* research.bib
  * A LaTeX bibliographic listing of the papers that helped us define our approach. Little, if anything, was used directly
