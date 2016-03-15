# Towards Automatic Ontology Building
CPE-581

Winter 2016

Description: Scrapetology is a web application with tools written in python to allow
for the gathering of data, restructuring of data into an ontology, and querying of the
data via web interface. The ontology is ultimately hosted on a website which allows

Using the web interface:

The Scrapetology web interface was created using Flask and can be hosted on any server
technology such as Nginx and Apache. The web interface consists of a simple form
that can be provided with natural language questions in the forms enumerated below.

The views.py file in the swpedia folder must be modified so it points to a hosted
ontology either online or on a local machine. There is an example provided for 
the starwars dbpedia at jamesbilous.com/static/test.owl.

Currently, queries in the following forms are allowed
	"What are instances of X" - where X is a class field that exists as a "subclassOf"
	property of a triple in the scraped ontology. Underscores can be ommitted in favor of spaces. 

Team Members:
* James Bilous
* Jon Doughty
* Jeff McGovern
