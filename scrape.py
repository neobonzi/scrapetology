from lxml import html
import requests

page = requests.get('https://en.wikipedia.org/wiki/List_of_American_Civil_War_battles')
tree = html.fromstring(page.content)

battles = tree.xpath('//table[2]/tr/td[1]/a[1]/text()')
battleLinks = tree.xpath('//table[2]/tr/td[1]/a[1]/@href')
startDates = tree.xpath('//table[2]/tr/td[2]/span[2]/text()')
states = tree.xpath('//table[2]/tr/td[3]/a[1]/text() | //table[2]/tr/td[3]/text()[not(../a) and 1]')
cwsac = tree.xpath('//table[2]/tr/td[4]/center/text()')

tuples = zip(battles, startDates, states, cwsac, battleLinks)
for item in tuples:
    print(item[0] + " - " + item[1] + " - " + item[2] + " (" + item[3] + ")" + "\n\t" + item[4]) 

