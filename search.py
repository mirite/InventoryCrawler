from bs4 import BeautifulSoup as BeautifulSoup
import requests
import json
import os.path
from os import path
import certifi
import urllib3
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

import config
import search_config

output = []
skips = []
i = 0
x = 0
hit_count = 0
hit_pages = 0

if not os.path.exists(config.site_name + '/cache'):
    os.makedirs(config.site_name + '/cache')

print("Starting search for term: '" + search_config.search + "'")

pages=json.load(open(config.site_name + '/pages.json'))

for page in pages:

    url = page['address']

    if len(url) == 0 or "#" in url:
        skips.append(url)
        continue

    #print("Checking: " + url)

    try:

        content = ""
        cache_path = config.site_name + "/cache/" + page['title'] + ".dat"

        if(search_config.use_cache and path.exists(cache_path)):
            
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
        if(not search_config.case_sensitive):
            content=content.lower()
            search_config.search = search_config.search.lower()
            
        if(search_config.search in content) :
            hit_count = hit_count + content.count(search_config.search)
            hit_pages = hit_pages + 1
            output.append("URL:" + url + " Len:" + str(content.count(search_config.search)))
    
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
