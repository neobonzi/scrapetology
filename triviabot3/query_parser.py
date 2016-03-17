#!/usr/bin/env python3

import sys

class QueryParser(object):
    def __init__(self):
        return
    def __str__(self):
        return self.__class__.__name__
    def get_query(self, input):
        assert(False)

class SPARQLQueryParser(QueryParser):
    QUERY_FORMAT='%s'

    def get_query(self, input):
        return self.QUERY_FORMAT % input

class WikiInputParser(SPARQLQueryParser):
    def format_entity(self, entity):
        return entity.strip().replace(' ', '_')
    def get_query(self, input):
        return self.QUERY_FORMAT % self.format_entity(input)

class WikiOutputParser(SPARQLQueryParser):
    def unformat_entity(self, entity):
        output = entity.strip()
        output = output.replace('Category_', 'Category:')
        output = output.replace('_', ' ')
        return output

class WikiQueryParser(WikiInputParser, WikiOutputParser):
    def blank_function(self):
        return

class ImmediateParentsParser(WikiQueryParser):
    QUERY_FORMAT = '''SELECT ?title
        WHERE {
            swdb:%s rdfs:subClassOf ?subject .
            ?subject owl:title ?title .
        }'''

class ImmediateChildrenParser(WikiQueryParser):
    QUERY_FORMAT = '''SELECT ?title
        WHERE {
            ?subject rdfs:subClassOf swdb:%s .
            ?subject owl:title ?title .
        }'''

class AllParentsParser(WikiQueryParser):
    QUERY_FORMAT = '''SELECT ?title
        WHERE {
            swdb:%s rdfs:subClassOf* ?subject .
            ?subject owl:title ?title .
        }'''

class AllChildrenParser(WikiQueryParser):
    QUERY_FORMAT = '''SELECT ?title
        WHERE {
            ?subject rdfs:subClassOf* swdb:%s .
            ?subject owl:title ?title .
        }'''

def main():
    bleh = QueryParser()
    meh = SPARQLQueryParser()
    wiki = WikiQueryParser()
    pare = ImmediateParentsParser()
    chil = ImmediateChildrenParser()
    all_pare = AllParentsParser()
    all_chil = AllChildrenParser()
    print(bleh)
    print(meh)
    print(wiki)
    print('{}:::{}'.format(wiki,wiki.get_query('Kylo Ren')))
    print('{}:::{}'.format(pare,pare.get_query('Kylo Ren')))
    print('{}:::{}'.format(chil,chil.get_query('Kylo Ren')))
    print('{}:::{}'.format(all_pare,all_pare.get_query('Kylo Ren')))
    print('{}:::{}'.format(all_chil,all_chil.get_query('Kylo Ren')))
    return 0
if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
