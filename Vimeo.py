import requests,os
import urllib,lxml
from requests.exceptions import ProxyError
from requests import Session
import lxml,json
import random
from bs4 import BeautifulSoup
import pickle

def save_json(idd,title,description,time,duration):
  if not os.path.exists(paths+"/"+str(idd) + '.json'):
    obj = {'data': []}
    obj['data'].append({'id': idd})
    obj['data'].append({'title': title})
    obj['data'].append({'description': description})
    obj['data'].append({'time': time})
    obj['data'].append({'duration': duration})
    obj['data'].append({'url': 'https://vimeo.com/'+str(idd)})
    with open(str(idd) + '.json', 'w') as outfile:
      json.dump(obj, outfile)
    os.rename(str(idd) + '.json', paths+"/"+ str(idd) + '.json')
    print("{} Saved".format(idd))
  else:
    print("Skipping (Already There)")

def save_thumbnail(idd,screenshot):
  if not os.path.exists(paths+"/"+str(idd) + '.jpg'):
    urllib.request.urlretrieve(screenshot, str(idd) + ".jpg")
    os.rename(str(idd) + ".jpg", paths +"/"+str(idd)+".jpg")


def ajax(id):
  #print(id)
  if not os.path.exists(paths+"/"+str(id)+".url"):
    try:
      m_url='https://vimeo.com/'+str(id)
      session.head(m_url)
      url=m_url+'?action=load_contextual_clips&page=1&stream_pos=0&offset=0'
      response = session.get(url=url,headers={'Referer':m_url,'X-Requested-With':'XMLHttpRequest'},proxies=proxy)
      soup = response.json()
      open(paths+"/"+str(id)+".url", 'a').close()
    except ProxyError:
      print("Proxy Error !!")
      #proxy={'https': random.choice(all_proxy)}
      #print(proxy)
      ajax(id)
      soup={}
      soup['clips']=[]
    for i in soup["clips"]:
      try:
        idd=i["id"]
      except:
        idd=""
      try:
        title=i["title"]
      except:
        title=""
      try:
        description=i["description"]
      except:
        description=""
      try:
        time=i["uploaded_on"]
      except:
        time=""
      try:
        duration=i["duration"]["formatted"]
      except:
        duration=""
      try:
        screenshot=i["thumbnail"]["src_2x"]
      except:
        screenshot=""
      save_json(idd,title,description,time,duration)
      save_thumbnail(idd,screenshot)
      #print(id==str(idd))
      if str(id) != str(idd):
        #print(id,idd)
        ajax(str(idd))
  else:
    print("URL opened")

paths="vimeo"
if not os.path.exists(paths):
  os.makedirs(paths)
session = Session()
headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36','referer':'https://vimeo.com/291276774'}
#proxy={'https': '199.168.141.147:19018'}
proxy={'https': '159.89.122.76:3128'}

with open("new_urls.pkl", 'rb') as f:
  mynewlist = pickle.load(f)
#print(len(mynewlist))
for every_id in mynewlist:
  try:
    ajax(every_id)
  except:
    pass
