#! /usr/bin/env python3

from urllib import request

en_wiki_export_base='https://en.wikipedia.org/wiki/Special:Export/'
def retrieve_xml(suffix_list):
    if isinstance(suffix_list, str):
        suffix_list = [suffix_list]
    assert(isinstance(suffix_list, (tuple, list, set)))
    for suffix in suffix_list:
        xml_url = '{}{}'.format(en_wiki_export_base, suffix)

        site = request.urlopen(xml_url)
        data = site.read()
        with open(suffix + '.xml', 'wb') as file:
            file.write(data)
def main():
    print('Please only use this as a library.')
    return 0

if __name__ == '__main__':
    rtn = main()
    sys.exit(rtn)
