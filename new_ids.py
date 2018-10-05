import requests, os
import urllib, lxml
from requests.exceptions import ProxyError
from requests import Session
import lxml, json
import random
from bs4 import BeautifulSoup
import pickle


def proxy():
    html = requests.get('https://www.sslproxies.org/')
    soup = BeautifulSoup(html.text, 'lxml')
    proxies_table = soup.find(id='proxylisttable')
    for row in proxies_table.tbody.find_all('tr'):
        proxy = row.find_all('td')[0].string + ':' + row.find_all('td')[1].string
        all_proxy.append(proxy)


def data(of):
    url = "https://vimeo.com/explore_data?action=videos&page_offset={}&context_id=927&context_type=channel".format(of)
    session.head('https://vimeo.com/watch')
    response = session.get(url=url,
                           headers={'Referer': 'https://vimeo.com/watch', 'X-Requested-With': 'XMLHttpRequest'},
                           proxies=proxy)
    soup = response.json()
    # print(soup)
    chk = 0
    try:
        chk = soup['videos']
        chk = 1
    except:
        pass

    if chk == 0:
        print("No Videos")
        return False
    else:
        if soup['videos'] == []:
            return False
        else:
            print("Found")
            try:
                for i in soup['videos']:
                    dta.append(i['clip_id'])
                    #print(i['clip_id'])
            except:
                try:
                    for i in soup['videos']:
                        dta.append(soup['videos'][i]['clip_id'])
                        #print(soup['videos'][i]['clip_id'])
                except:
                    pass
            return True


session = Session()
dta = []
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'referer': 'https://vimeo.com/291276774'}

all_proxy = []
proxy()
proxy = {'https': '199.168.141.147:19018'}
i = 0

data(i)

with open('new_urls.pkl', 'wb') as f:
    pickle.dump(dta, f)
