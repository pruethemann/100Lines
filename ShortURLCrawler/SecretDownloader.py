## Bitly crawler
import requests
import random
import time
import csv
import re
from bs4 import BeautifulSoup

def importCodes(filename):
    codes = []
    with open(filename, 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        c = 0
        for row in reader:
            codes += row[0].split(' ')
    return codes

def request(url, code):
    try:
        page = requests.get(url + code)

    except Exception as e:
        print(f'Error: {e}')




url = 'http://www.t1p.de/'

codes = importCodes('T1p.txt')

for code in codes:
    response = requests.get(url + code)
    print(response.url)


"""
for code in codes:
    site = url + code

    response = requests.get(site)

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    urls = [img['src'] for img in img_tags]


    for url in urls:
        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
        if filename == None:
            continue
        with open(f'./Download/' + filename.group(1), 'wb') as f:
            if 'http' not in url:
                # sometimes an image source can be relative
                # if it is provide the base url which also happens
                # to be the site variable atm.
                url = '{}{}'.format(site, url)
            response = requests.get(url)
            f.write(response.content)
"""