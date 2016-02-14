from lxml import html
import requests

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
    
    # testing only 3 battles for now
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

if __name__ == '__main__':
    battles = scrape_battles()
    # print 'battles: ', battles[:3]
    scrape_generals(battles)