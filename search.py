from bs4 import BeautifulSoup as BeautifulSoup
import requests
import json
import os.path
from os import path

search = "compost"
use_cache = True
output = []
skips = []
i = 0

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

    print("Checking: " + url)
    try:

        content = ""

        if(use_cache and path.exists("cache/" + page['title'] + ".dat")):
            with open("cache/" + page['title'] + ".dat", "r") as cache_file:
                content = cache_file.read()
        else:
            response = requests.get(url, verify=False)
            content = response.content

            with open("cache/" + page['title'] + ".dat", "w") as cache_file:
                cache_file.write(content.url + "\n----\n" + content.text)
                i = i + 1

        #soup = BeautifulSoup(content.text, 'html.parser')
        #results = soup.find_all(search)
        if(search in content) :

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
