import json

#File/operating system related imports
import os
import sys

import os.path
from os import path

#Network request related imports
import certifi
import requests
import urllib3

from bs4 import BeautifulSoup as BeautifulSoup #Used for page navigation

#Make sure SSL is configured
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

site_name = "rootree"

#Load the site info from the crawler
config_path = site_name + '/info.json'

if(path.exists(config_path)):
    info=json.load(open(config_path))
else:
    sys.exit("Site config not found")

domain = info['path']
stamp = info['created']

page_list = site_name + '/pages.json'

if(path.exists(page_list)):
  pages=json.load(open(page_list))
else:
  sys.exit("Page list missing for " + site_name + " please recrawl")

#Loop through all pages
for page in pages:

    cache_path = site_name + "/cache/" + page['title'] + ".dat"
    with open(cache_path, "r") as cache_file:
        content = cache_file.read()
        soup = BeautifulSoup(content, 'html.parser')
        for a in soup.find_all('div'):
            print(str(a))
print("Done!")