from lxml import html
import requests
import re

wikipediaBaseURI = 'https://en.wikipedia.org'

def scrape_battles():
    data = {}
    page = requests.get('https://en.wikipedia.org/wiki/List_of_American_Civil_War_battles')
    tree = html.fromstring(page.content)
    tree.make_links_absolute(wikipediaBaseURI)

    ## Extract general battle data
    battles = tree.xpath('//table[2]/tr/td[1]/a[1]/text()')
    battleLinks = tree.xpath('//table[2]/tr/td[1]/a[1]/@href')
    startDates = tree.xpath('//table[2]/tr/td[2]/span[2]/text()')
    states = tree.xpath('//table[2]/tr/td[3]/a[1]/text() | //table[2]/tr/td[3]/text()[not(../a) and 1]')
    cwsac = tree.xpath('//table[2]/tr/td[4]/center/text()')

    # print 'battles: ', battleLinks

    tuples = zip(battles, startDates, states, cwsac, battleLinks)
    for item in tuples:
        data[item[0]] = { 'startDate' : item[1], 'state' : item[2], 'cwsac' : item[3], 'url' : item[4]}

    for key in data:
        value = data[key]
        # print(key + " - " + value['startDate'] + " - " + value['state'] + " (" + value['cwsac'] + ")" + "\n\t" + value['url']) 
    
    ## Visit battle pages and extract mroe data

    #for key in data:
    #    battlePage = requests.get(data[key][url])
    #    tree = html.fromstring(page.content)
    #    tree.make_links_absolute(wikipediaBaseURI)

    return battleLinks

def scrape_generals(battles):
    generals = {}
    
    # testing only 5 battles for now - good to 5
    # test 5-10
    for battle in battles:
        names = []
        links = []
        result = []
        page = requests.get(battle)
        tree = html.fromstring(page.content)
        tree.make_links_absolute(wikipediaBaseURI)
        for a in range(1,4):
            link_str = '//table//tr[7]//a[%d]//@href' % a
            links = links + tree.xpath(link_str)
            name_str = '//table//tr[7]//td/a[%d]//text()' % a
            names = names + tree.xpath(name_str)
        
        result = zip(names, links)
        for name,link in result:
            if not 'redlink=1' in link:
                generals[name] = link
        del names[:]
        del links[:]
        del result[:]
        
    print generals
    print 'size dictionary: ', len(generals)
    return generals

def input_generals():
    generals = {}
    with open('list_generals.txt','r') as file_in:
        for line in file_in:
            (key, value) = line.split(":", 1)
            # print 'key: ', key[1:-1]
            # print 'value: ', value[2:-4]
            generals[key[1:-1]] = value[2:-4]
    return generals

from bs4 import BeautifulSoup as bs

def scrape_generals(generals_dict):
    print 'link: ', generals_dict.values()[1]
    respond = requests.get(generals_dict.values()[1])
    soup = bs(respond.text)
    # print 'bday: ', t.find(class="bday")
    
    rows = soup.find("table").find("tbody").find_all("tr")
    # rows = soup.find("table")
    for row in rows:
        print row
    #     cells = row.find_all("td")
    #     rn = cells[0].get_text()
    #     print rn
    # and so on
    # print 'bday: ', soup.title
    # for i in t:
    #     try:
    #         # print i.find('span').get_text()[-5:], i.find('a').get_text()
    #         print i
    #     except AttributeError:
    #         pass    
    
        
if __name__ == '__main__':
    # battles = scrape_battles()
    # print 'battles: ', battles[:3]
    # scrape_generals(battles)
    generals = input_generals()
    scrape_generals(generals)