import json

#File/operating system related imports
import os.path
import sys
from os import path

#Network related imports
import certifi
import requests
import urllib3

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where()) #To securely crawl SSL sites
case_sensitive = False #Config options that can't be changed during runtime currently
output = [] #Hit pages
skips = [] #Pages that couldn't be searched
sites = [] #Sites available to search
new_files_read = 0
cache_files_read = 0
hit_count = 0
hit_pages = 0
domain = ""
stamp = ""

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

  p=os.listdir(".")
  for i in p:
    if os.path.isdir(i) and i[0] != "." and i[0] != "_":
        if(path.exists(i + "/info.json")):
            sites.append(i)
            print(i)

print("Rootree Search Tool")

#Decide if using args or prompting for options
if(len(sys.argv) >= 2):

  site_name = str(sys.argv[1])
  search = str(sys.argv[2])
  use_cache = True

  load_config()

  print("Last crawled " + domain + " at " + stamp)

else:

  print("Please select a crawled site.\nSites available:")
  
  list_sites()

  site_entry = input("What name is the site saved as? ")

  #ideally reprompt for entry, currently crash if site not valid
  if(not site_entry in sites):
      sys.exit("Site not found")
  else:
    site_name = site_entry

  load_config()

  print("Last crawled " + domain + " at " + stamp)

  search = input("What are you looking for? ")

  cache_prompt = input("Do you want to use the cached files? ")

  if( "y" in cache_prompt.lower() ):
    use_cache = True
  else:
    use_cache = False

#Make sure the cache directory is ready to use
if not os.path.exists(site_name + '/cache'):
    os.makedirs(site_name + '/cache')

print("Starting search for term: '" + search + "'")

page_list = site_name + '/pages.json'

if(path.exists(page_list)):
  pages=json.load(open(page_list))
else:
  sys.exit("Page list missing for " + site_name + " please recrawl")

#Loop through all pages
for page in pages:

    url = page['address']

    #Check that we aren't searching non-existent or link pages
    if len(url) == 0 or "#" in url:
        skips.append(url)
        continue
    
    #A nice try statement in case network fails
    try:

        content = ""
        cache_path = site_name + "/cache/" + page['title'] + ".dat"

        #If using cached files and the cache for the specific page exists
        if(use_cache and path.exists(cache_path)):

            with open(cache_path, "r") as cache_file:
                content = cache_file.read()
                cache_files_read = cache_files_read + 1
        else:
            #Grab page contents
            response = requests.get(url)
            content = str(response.content)

            #Create cache file of page
            with open(cache_path, "w") as cache_file:
                cache_file.write(url + "\n----\n" + content)
                new_files_read = new_files_read + 1

        #Convert content so that non case sensitive matching is possible
        if(not case_sensitive):
            content=content.lower()
            search = search.lower()
        
        #This is the actul search condition
        if(search in content) :
            hit_count = hit_count + content.count(search)
            hit_pages = hit_pages + 1
            output.append("URL:" + url + " Len:" + str(content.count(search)))
    
    except Exception as e:
      #Track the pages that could be checked
      skips.append(url)
      print("Request failed for " + url + " " + str(e))

print("Done!")

print(str(len(skips)) + " Skipped Pages")
for result in skips:
    print(result)

print(str(len(output)) + " Matching Pages")
for result in output:
    print(result)

print(str(hit_pages) + " Page Hits")
print(str(hit_count) + " Total Hits")
print(str(new_files_read) + " New Pages Checked")
print(str(cache_files_read) + " Cached Pages Checked")