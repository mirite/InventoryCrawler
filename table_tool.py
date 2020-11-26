########
# Imports
#######
import json

#File/operating system related imports
import os
import sys

import os.path
from os import path

from bs4 import BeautifulSoup as BeautifulSoup #Used for page navigation

########
# Variables and config
#######


cache_path = "rootree/converted/pagesdielines/_pagesdielines.html"
content = ""
output = ""

with open(cache_path, "r", encoding="utf-8") as cache_file:
    content = cache_file.read()

soup = BeautifulSoup(content, 'html.parser')

tables = soup.find_all("table")

for table in tables:
    output = output + "--------"
    rows = table.find_all("tr")
    for row in rows:
        output = output + "\n\n\n"

        cell = row.find("td")

        size = cell.text
        output=output + "Size: " + size + "\n-\n"

        cell.extract()
        cell = row.find("td")
        x = 0
        y = 0
        pairs = []
        results = True

        while(results):
            
            label = ""
            url = ""

            span = cell.find("span")
            if (span):
                #print(str(span))
                label = str(span.text)
                label = label.strip()
                span.extract()

            a = cell.find("a")
            if (a):
                popped = str(a['href']).split("/")
                print(str(popped))
                url = popped[len(popped) - 1]
                a.extract()
            
            if label != "" and url != "":
                pairs.append({label : url})
                output = output + label + " " + url + "\n"
            else:
                results = False
            #print(str(pairs))


a = BeautifulSoup(output, 'html.parser')
output = a.prettify(formatter="minimal")
with open("table.html", "w", encoding="utf-8") as cache_file:
    cache_file.write(output)