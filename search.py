from bs4 import BeautifulSoup as BeautifulSoup
import requests
import json
import os.path
from os import path

search = "pages/why-flexible"
use_cache = True
output = []
skips = []
i = 0
x = 0
hit_count = 0
hit_pages = 0

print("Starting search for term: '" + search + "'")

pages=json.load(open('trims.json'))

for page in pages:

    url = page['address']

    if len(url) == 0 or "#" in url:
        skips.append(url)
        continue

    if url[0] == "/":
        url = "https://rootree.ca" + url
    if not "http" in url:
        url = "https://rootree.ca/" + url

    #print("Checking: " + url)

    try:

        content = ""
        cache_path = "cache/" + page['title'] + ".dat"

        if(use_cache and path.exists(cache_path)):
            
            #print("Using cached page " + cache_path)

            with open(cache_path, "r") as cache_file:
                content = cache_file.read()
                x = x + 1
        else:
            response = requests.get(url, verify=False)
            content = str(response.content)

            with open(cache_path, "w") as cache_file:
                cache_file.write(url + "\n----\n" + content)
                i = i + 1

        #soup = BeautifulSoup(content.text, 'html.parser')
        #results = soup.find_all(search)
        #print(content)
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
