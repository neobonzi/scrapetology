#! /usr/bin/env python3

import os
import sys
import logging
import pyparsing

sys.path.append(os.getcwd())
import wikitools
from args import args_parse_xml

def main():
    arg_parser = args_parse_xml()
    args = arg_parser.parse_args()
    with open(args.filename, 'r', encoding='latin1') as file:
        thecontent = pyparsing.Word('' + pyparsing.alphanums) | '+' | '-'
        parens     = pyparsing.nestedExpr( '{', '}', content=thecontent)
        file_str = ''
        for line in file:
            file_str += line.replace('\n','')
        print(file_str)
        parens.parseString(file_str)
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
