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
import urllib

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where()) #To securely crawl SSL sites
skips = [] #images that couldn't be searched
sites = [] #Sites available to search
domain = ""
stamp = ""
site_count = 0 #Number of sites available
image_index = 0

#Loads the configuration info from selected site
def load_config():

  global domain
  global stamp

  #Load the site info from the crawler
  config_path = site_name + '/info.json'

  if(path.exists(config_path)):
    info=json.load(open(config_path))
  else:
    sys.exit("Site config not found")

  domain = info['path']
  stamp = info['created']

#Lists the sites available and logs them to sites[]
def list_sites():

  global sites
  global site_count

  p=os.listdir(".")
  for i in p:
    if os.path.isdir(i) and i[0] != "." and i[0] != "_":
        site_path = i + "/info.json"
        if(path.exists(site_path)):
          site_count = site_count + 1
          info=json.load(open(site_path))
          sites.append({"id":site_count,"name":i,"url":info['path'],"created":info['created']})
          print(str(site_count) + ". " + i + " - Domain: " + info['path'] + " - Crawled: " + info['created'])

print("\n##########\n# Rootree Image Tool\n##########")

print("\nPlease select a crawled site.\n\nSites available:")
  
list_sites()

site_entry = int(input("\nWhat site do you want to search? "))

#ideally re-prompt for entry, currently crash if site not valid
if(site_entry > site_count or site_entry == 0):
    sys.exit("Site not found")
else:
    site_name = sites[site_entry - 1]['name']

domain = sites[site_entry - 1]['url']
stamp = sites[site_entry - 1]['created']

#Make sure the cache directory is ready to use
if not os.path.exists(site_name + '/images'):
    os.makedirs(site_name + '/images')

print("\nStarting search for images")

image_list = site_name + '/images_log.txt'

if(path.exists(image_list)):
    with open(image_list) as image_text:
        images=image_text.readlines()
else:
  sys.exit("Image list missing for " + site_name + " please re-crawl")

image_count = len(images)
print(image_count, "images to download")
#Loop through all images
for image in images:
    try:
        split_src = image.split(".")
        file_type = "." + split_src[len(split_src)-1]
        new_path = site_name + "/images/" + "image_" + str(image_index) + file_type
        urllib.request.urlretrieve(image, new_path)
        image_index = image_index + 1
        print("Downloaded",image_index,"of",image_count)
    except Exception as e:
        print("Error processing",image,e)

print("Done!")