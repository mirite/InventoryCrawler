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

if not os.path.exists(site_name + '/converted'):
  os.makedirs(site_name + '/converted')

total_changes = 0

#Loop through all pages
for page in pages:

    cache_path = site_name + "/cache/" + page['title'] + ".dat"
    with open(cache_path, "r") as cache_file:

        content = cache_file.read()
        soup = BeautifulSoup(content, 'html.parser')

        
        
        #Only deal with pages with shogun content
        for a in soup.find_all("div", "shogun-root"):

          title = page['title']
          title = title.replace("httpsrootreedotca","") #fix hardcode value

          

          print("Converting page ", title)

          #Remove link tags and scripts from the page
          [s.extract() for s in a('script')]
          [s.extract() for s in a('link')]

          changes = 0

          while (True):

            previous_changes = changes

            for d in a('div'):
              if(len(d.contents) == 0):
                d.extract()
                changes = changes + 1
            
            for s in a('span'):
              if(len(s.contents) == 0):
                s.extract()
                changes = changes + 1
            
            #Only leave loop if there were no additional changes
            if(changes == previous_changes):
              break

          total_changes = total_changes + changes

          converted_path = site_name + "/converted/" + title + ".html"

          with open(converted_path,"w") as output:

            output.write(a.prettify(formatter="minimal"))

print("Done! ", str(total_changes), " empty elements removed")