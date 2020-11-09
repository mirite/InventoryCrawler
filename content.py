########
# Imports
#######
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

########
# Helper Functions
#######

#Remove unwanted attributes from parent tag
def strip_meta(a):
  del a['class']
  del a['id']
  del a['data-region']
  del a['data-shogun-id']
  del a['data-shogun-page-id']
  del a['data-shogun-page-version-id']
  del a['data-shogun-platform-type']
  del a['data-shogun-site-id']
  del a['data-shogun-variant-id']
  del a['data-col-grid-mode-on']

#Remove divs and pretty up the html for writing
def strip_structure(html):
  content = html.replace("<div>","")
  content = content.replace("</div>","")
  content = ' '.join(content.split()) #get rid of excess white space
  content_soup = BeautifulSoup(content, 'html.parser')
  return content_soup.prettify(formatter="minimal")

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

  if not os.path.exists(site_name + '/converted'):
    os.makedirs(site_name + '/converted')

  if not os.path.exists(site_name + '/converted/content'):
    os.makedirs(site_name + '/converted/content')
  return pages


########
# Variables and config
#######

#Make sure SSL is configured
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

site_name = "rootree"
domain = ""
stamp = ""
total_changes = 0
singles = 0

########
# Main body
#######


print("\n##########\n# Rootree Shogun Tool\n##########")

#Load the site info from the crawler
config = load_config(site_name)
pages = get_pages(config)

print("Converting pages from",config['path'],"crawled on",config['created'],"\n")

#Loop through all pages
for page in pages:

  try:
    cache_path = site_name + "/cache/" + page['title'] + ".dat"
    with open(cache_path, "r") as cache_file:

        content = cache_file.read()
        content=content.replace('style=""',"")

        soup = BeautifulSoup(content, 'html.parser')

        passes = 0 #Right now I'm doing three passes with no changes
        
        #Only deal with pages with shogun content
        for a in soup.find_all("div", "shogun-root"):

          title = page['title']
          title = title.replace("httpsrootreedotca","") #fix hardcode value
          
          print("Converting page", title)

          #Remove link tags and scripts from the page
          [s.extract() for s in a('script')]
          [s.extract() for s in a('link')]
          strip_meta(a)

          changes = 0
          previous_changes = -1 #If we default to zero the loop won't run

          while (changes != previous_changes):

            previous_changes = changes

            for d in a('div'):

              strip_meta(d)

              child_count = len(list(d.findChildren("div", False)))
              #print(str(child_count) + " children. ") #+ str(d.contents))

              #if(child_count < 5):
              #  for child in d.findChildren("div", False):
              #    print("Child: " + str(child.contents) + "\n\n")

              if(len(d.contents) == 0):
                d.extract()
                changes = changes + 1
              elif(child_count == 1):
                d.unwrap()
                #print(str(d.children))
                #d.replace_with(list(d.children)[0])
                changes = changes + 1
                singles = singles + 1

            for s in a('span'):
              if(len(s.contents) == 0):
                s.extract()
                changes = changes + 1
            
          total_changes = total_changes + changes

          converted_path = site_name + "/converted/" + title + ".html"
          content_path = site_name + "/converted/content/" + title + ".html"

          html = a.prettify(formatter="minimal")
          content = strip_structure(html)

          with open(converted_path,"w") as output:
            output.write(html)

          with open(content_path,"w") as output:
            output.write(content)

    #break #Uncomment to test only first file for debug
  except Exception as e:
    print("Error processing",page['title'],e)

print("\nDone!", str(total_changes), "change made.", str(singles), "single child divs eliminated.\n")