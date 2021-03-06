import pypandoc
#File/operating system related imports
import os
import sys
import re

import os.path
from os import path
import json
from bs4 import BeautifulSoup as BeautifulSoup

site_name = "rootree"

#Load the site info from the crawler
def load_config(site_name):
  
  config_path = site_name + '/info.json'

  if(path.exists(config_path)):
      info=json.load(open(config_path))
  else:
      sys.exit("Site config not found")

  return info

#Returns the list of pages to convert
def get_pages(config):
  page_list = site_name + '/pages.json'

  if(path.exists(page_list)):
    pages=json.load(open(page_list))
  else:
    sys.exit("Page list missing for " + site_name + " please re-crawl")

  return pages

def get_path(config, page, ext):

    relative_path = page["address"].replace(config["path"],"").replace("\n","").strip()

    if(relative_path[0] == "/"):
        relative_path = relative_path[1:]

    
    if(len(relative_path) > 1 and "/" in relative_path):

        if(relative_path[len(relative_path)-1]) == "/":
            relative_path = relative_path[0:len(relative_path)-1]

        split_path = relative_path.rsplit("/",1)
        file_name = split_path[1]
        relative_path = split_path [0] + "/"
        
        if not ext in file_name:
            file_name = file_name + ext

    else:
        file_name = "index" + ext
        relative_path = ""

    return relative_path, file_name

def get_meta(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            temp = f.read()
    except Exception as e:
        print("Error getting meta",in_file,e)
        return ""
    
    soup = BeautifulSoup(temp, 'html.parser')
    #print(temp)
    meta = soup.find("meta",{"name":"description"})

    if(meta):
        return str(meta['content'])
    else:
        return "None"

print("\n##########\n# Rootree Word Tool\n##########")

#Load the site info from the crawler
config = load_config(site_name)
pages = get_pages(config)

base_out = site_name + "/word/"
base_in = site_name + "/converted/"

in_ext = ".html"
out_ext = ".docx"

for page in pages:

    print("Processing", page)

    rel_in_path, in_file = get_path(config, page, in_ext)
    rel_out_path, out_file = get_path(config, page, out_ext)

    in_path = base_in + rel_in_path + in_file
    out_path = base_out + rel_out_path + out_file

    if not os.path.exists(base_out + rel_out_path):
        os.makedirs(base_out + rel_out_path)
    
    try:
        with open(in_path, "r", encoding="utf-8") as f:
            temp = f.read()
    except Exception as e:
        print("Error",in_file,e)
        continue
    
    cache_path = site_name + "/cache/" + page['title'].replace("â€“","") + ".dat"
    meta = get_meta(cache_path)

    temp = "<a href='" + page['address'] + "'>" + page['address'] + "</a>" + "<br><br>Meta: " + meta + "<br><br>"  + temp
    temp = re.sub(r"<img [^>]+>","(Image)",temp)

    try:
        output = pypandoc.convert_text(temp, format='html', to='docx', outputfile=out_path, extra_args=['-RTS'])
    except Exception as e:
        print("Error",in_file,e)

print("Done!")