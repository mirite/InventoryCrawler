import pypandoc
#File/operating system related imports
import os
import sys
import re

import os.path
from os import path
import json

site_name = "rootree2"

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

    relative_path = page["address"].replace(config["path"],"")

    if(len(relative_path) > 0):

        if(relative_path[len(relative_path)-1]) == "/":
            relative_path = relative_path[0:len(relative_path)-1] + ext
        else:
            relative_path = relative_path + ext

    else:
        relative_path = "index" + ext

    return relative_path

print("\n##########\n# Rootree Word Tool\n##########")

#Load the site info from the crawler
config = load_config(site_name)
pages = get_pages(config)

base_out = site_name + "/word"
base_in = site_name + "/converted"

in_ext = ".html"
out_ext = ".docx"

if not os.path.exists(base_out):
    os.makedirs(base_out)

for page in pages:

    in_path = base_in + get_path(config, page, in_ext)
    out_path = base_out + get_path(config, page, out_ext)

    print(in_path, out_path)
    output = pypandoc.convert(source=in_path, format='html', to='docx', outputfile=out_path, extra_args=['-RTS'])