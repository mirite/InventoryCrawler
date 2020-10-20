from bs4 import BeautifulSoup as BeautifulSoup
import requests
import json

search = "1-877"
output = []
skips = []

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
        content = requests.get(url, verify=False)

        #soup = BeautifulSoup(content.text, 'html.parser')
        #results = soup.find_all(search)
        if(search in content.text) :

            output.append("URL:" + url + " Len:" + str(content.text.count(search)))
    
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
