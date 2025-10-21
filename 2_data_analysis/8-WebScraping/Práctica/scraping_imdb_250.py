from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import json
from fake_useragent import UserAgent

url = "https://www.imdb.com/chart/top/"

ua = UserAgent()
headers = {'User-Agent': ua.random}
response = requests.get(url, headers=headers)
soup = bs(response.content, 'html.parser')

my_top250 = {
            "Ranking": [],
            "Titulo": [],
            "Año": [],
            "Duración": [],
            "Rating": []
            }

for x in json.loads(soup.find("script", type="application/ld+json").get_text())['itemListElement']:
    my_top250['Titulo'].append(x['item'].get('alternateName', x['item'].get('name')))
    my_top250['Duración'].append(x['item']['duration'][2:])    
    my_top250['Rating'].append(x['item']['aggregateRating']['ratingValue'])
    
for p in json.loads(soup.find("script", id="__NEXT_DATA__").get_text())['props']['pageProps']['pageData']['chartTitles']['edges']:
    my_top250['Año'].append(p['node']['releaseYear']['year'])    
    my_top250['Ranking'].append(p['currentRank'])
    
my_top250 = pd.DataFrame(my_top250)
my_top250.to_csv("./data/top250.csv")

