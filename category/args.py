import argparse
import os
import sys

sys.path.append(os.getcwd())


class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        # this is the RawTextHelpFormatter._split_lines
        if text.startswith('R|'):
            return text[2:].splitlines()
        return argparse.HelpFormatter._split_lines(self, text, width)


def get_arg_parser(description):
    return argparse.ArgumentParser(prog=sys.argv[0],
                                   description=description,
                                   formatter_class=SmartFormatter
                                   )

DESC = 'Scrapes the category section of Star Wars to automatically build an ontology.'
def args_build_ontology(description=DESC):
    arg_parser = get_arg_parser(description)
    arg_parser.add_argument('-f', '--filename',
                            action='store',
                            metavar='<filename>',
                            help='wiki XML file',
                            required=True)
    return arg_parser

def args_build_graph():
  description = 'Uses data scraped from the Star Wars wikia website to generate a rdf/xml graph'
  arg_parser = get_arg_parser(description)
  req = arg_parser.add_argument_group('required arguments')

  req.add_argument('-f', '--filename',
                   required=True,
                   action='store',
                   metavar='<filename>',
                   nargs=1,
                   help='Filename for graph output')

  return arg_parser
