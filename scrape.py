from lxml import html
import requests

wikipediaBaseURI = 'https://en.wikipedia.org')

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

tuples = zip(battles, startDates, states, cwsac, battleLinks)
for item in tuples:
    data[item[0]] = { 'startDate' : item[1], 'state' : item[2], 'cwsac' : item[3], 'url' : item[4]}

for key in data:
    value = data[key]
    print(key + " - " + value['startDate'] + " - " + value['state'] + " (" + value['cwsac'] + ")" + "\n\t" + value['url']) 

## Visit battle pages and extract mroe data

#for key in data:
#    battlePage = requests.get(data[key][url])
#    tree = html.fromstring(page.content)
#    tree.make_links_absolute(wikipediaBaseURI)
