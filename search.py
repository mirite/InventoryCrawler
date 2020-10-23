from bs4 import BeautifulSoup as BeautifulSoup
import requests
import json
import os.path
from os import path
import certifi
import urllib3
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

import sys

if(len(sys.argv) >= 2):

  site_name = str(sys.argv[1])
  search = str(sys.argv[2])
  use_cache = True
  
  info=json.load(open(site_name + '/info.json'))

  domain = info['path']
  stamp = info['created']
  print("Last crawled " + domain + " at " + stamp)

else:
  print("Sites available:")
  
  p=os.listdir(".")
  for i in p:
    if os.path.isdir(i) and i[0] != "." and i[0] != "_":
        print(i)


  site_name = input("What name is the site saved as? ")

  info=json.load(open(site_name + '/info.json'))

  domain = info['path']
  stamp = info['created']
  print("Last crawled " + domain + " at " + stamp)

  search = input("What are you looking for? ")
  cache_prompt = input("Do you want to use the cached files? ")

  if( "y" in cache_prompt.lower() ):
    use_cache = True
  else:
    use_cache = False

print("Starting Search")

case_sensitive = False

output = []
skips = []
i = 0
x = 0
hit_count = 0
hit_pages = 0

if not os.path.exists(site_name + '/cache'):
    os.makedirs(site_name + '/cache')

print("Starting search for term: '" + search + "'")

pages=json.load(open(site_name + '/pages.json'))

for page in pages:

    url = page['address']

    if len(url) == 0 or "#" in url:
        skips.append(url)
        continue

    #print("Checking: " + url)

    try:

        content = ""
        cache_path = site_name + "/cache/" + page['title'] + ".dat"

        if(use_cache and path.exists(cache_path)):
            
            #print("Using cached page " + cache_path)

            with open(cache_path, "r") as cache_file:
                content = cache_file.read()
                x = x + 1
        else:
            response = requests.get(url)
            content = str(response.content)

            with open(cache_path, "w") as cache_file:
                cache_file.write(url + "\n----\n" + content)
                i = i + 1

        #soup = BeautifulSoup(content.text, 'html.parser')
        #results = soup.find_all(search)
        #print(content)
        if(not case_sensitive):
            content=content.lower()
            search = search.lower()
            
        if(search in content) :
            hit_count = hit_count + content.count(search)
            hit_pages = hit_pages + 1
            output.append("URL:" + url + " Len:" + str(content.count(search)))
    
    except Exception as e:
        skips.append(url)
        print("Request failed for " + url + " " + str(e))

print("Done!")

print(str(len(skips)) + " Skipped Pages")
for result in skips:
    print(result)

print(str(len(output)) + " Matching Pages")
for result in output:
    print(result)

print(str(hit_pages) + " Page Hits")
print(str(hit_count) + " Total Hits")
print(str(i) + " New Pages Checked")
print(str(x) + " Cached Pages Checked")
