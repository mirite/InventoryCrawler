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

size_output = ""
dieline_output = ""

cur_table = 0
ids = [5, 6, 7, 8, 9]
row_id = 1

with open(cache_path, "r", encoding="utf-8") as cache_file:
    content = cache_file.read()

soup = BeautifulSoup(content, 'html.parser')

tables = soup.find_all("table")

for table in tables:
    rows = table.find_all("tr")
    for row in rows:

        cell = row.find("td")

        size = cell.text

        if("Dimension" in size): #Skip the header rows
            continue

        size_comps = size.split("\n")
        size_comps = list(map(str.strip, size_comps))
        size_comps = list(filter(None, size_comps))

        size_name = size_comps[0]
        size_description = "<br>".join(size_comps[1:])

        size_output=size_output + "INSERT INTO wp_rt_dl_sizes (id, added, user_id, display_name, cat_description, cat_id) VALUES (" + str(row_id) + ", NOW(), 3,'" + str(size_name) + "','" + size_description + "'," + str(ids[cur_table]) + ");\n"

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
                #print(str(popped))
                url = popped[len(popped) - 1].split("?")[0]
                url = "/wp-content/uploads/dielines/" + url
                a.extract()
            
            if label != "" and url != "":
                pairs.append({label : url})
                dieline_output = dieline_output + "INSERT INTO wp_rt_dl_dielines (added, user_id, display_name, file_path, size_id) VALUES(NOW(), 3, '" + label + "', '" + url + "'," + str(row_id) + ");\n"
            else:
                results = False
            #print(str(pairs))
        row_id = row_id + 1
    cur_table = cur_table + 1


with open("output.sql", "w", encoding="utf-8") as cache_file:
    cache_file.write(size_output + dieline_output)