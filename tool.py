import csv
import datetime

#File/operating system related imports
import os
import sys

#Network request related imports
import certifi
import requests
import urllib3

from bs4 import BeautifulSoup as BeautifulSoup #Used for page navigation

#Make sure SSL is configured
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

#A debug tool to see what rule is failing when detecting links
debug_detection = False

#Helper functions
#Creates the page list file
def create_json(found):
  out = "["
  for obj in found:
    url = obj['Link']
    title = create_title(url)
    out=out+'{"title":"' + title + '","address":"' + url + '"},'
  out=out[:-1] + ']'
  return out

#Saves the content of the logs
def create_log(file_list, name):
  with open(site_name + "/" + name + "_log.txt",'w', newline='') as rejectedLog:
    for item in file_list:
      rejectedLog.write(item + "\n")
    print("Wrote to " + site_name  + "/" + name + "_log.txt")

#Makes a safe string of the url
def create_title(url):
  title=url.replace("/","")
  title=title.replace(".","dot")
  title=title.replace("?","query")
  title=title.replace(":","")
  return title


#Core code
if(len(sys.argv) >= 2):

  domain = str(sys.argv[1])
  site_name = str(sys.argv[2])

else:
  domain = input("What is the domain you want to crawl (https://example.com)? ")
  site_name = input("What name do you want to save the logs under? ")

#Make sure the found list is ready to write
#Deprecated
fileName = site_name + "/found-pages.csv"
f = open(fileName, "w+")
f.close()

#Make sure the site directory and site cache are ready to write
if not os.path.exists(site_name):
  os.makedirs(site_name)

if not os.path.exists(site_name + '/cache'):
  os.makedirs(site_name + '/cache')

#List of pages to start
page_list=[]
page_list.append({"Link":domain})

pages_checked_counter = 0
page = 0
fails_in_a_row = 0

found = [] #Found links that are valid
rejected = [] #Links that don't meet criteria to follow
missing = [] #Broken links
scripts = [] #Linked scripts
images = [] #Linked images

#Work through list of pages, will epand over time
for link_object in page_list:

  url = link_object['Link'] #the current page to check 
  print('Searching: ',url)

  try:

    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    fails_in_a_row = 0 #Reset failed request meter

  except:

    fails_in_a_row = fails_in_a_row + 1
    print('Request Failed ', fails_in_a_row)

    if(fails_in_a_row>10):

      print('Giving Up')
      break

    else:

      page_list.append({"Link":url})
      continue
  
  #Page is giving error, log it
  if (page.status_code != 200):

    missing.append(url + " returned code " + str(page.status_code))
  
  #Parse the HTML
  soup = BeautifulSoup(page.text, 'html.parser')

  #Create cache file
  cache_path = site_name + "/cache/" + create_title(url) + ".dat"

  with open(cache_path, "w") as cache_file:
    cache_file.write(url + "\n----\n" + page.text)

  #Loop through script tags on the page
  for a in soup.find_all('script', src=True):

    #Only add new scripts
    if not a['src'] in scripts:
      scripts.append(a['src'])

  #Loop through images on page
  for a in soup.find_all('img', src=True):

    #Only add new images
    if not a['src'] in images:
      images.append(a['src'])
  
  #Loop through all links on page
  for a in soup.find_all('a', href=True):
   
    l = a['href'] #Contents of link tag

    #Make sure href exists ie. not href=""
    if l:

      #Various checks to make sure link should be followed
      link_in_scope = (domain in l or l[0] == "/" or not "http" in l)
      link_not_an_anchor = l[0] != "#"
      link_valid_type = not ".png" in l and not ".jpg" in l and not ".pdf" in l and not ".webp" in l and not ".svg" in l and not "tel:" in l and not "javascript:void" in l and not "mailto:" in l and not "fax:" in l and not "ts3server:" in l and not "callto:" in l
      link_not_excluded_dir = not "/uploads/" in l

      #Store a copy of unprocessed link
      raw_link = l

      if(debug_detection):
        print(l)
        print(link_in_scope)
        print(link_not_an_anchor)
        print(link_valid_type)
        print(link_not_excluded_dir)

      #Append domain if link is relative
      if not domain in l:

        #Deal with root links
        if(l[0] != "/"):
          l = "/" + l

        link = {'Link':domain + l}

      else:

        link = {'Link':l}

      #Make sure all checks passed and that page hasn't already been checked
      if link_not_an_anchor and link_in_scope and link_valid_type and link_not_excluded_dir and not link in found:
          
          page_list.append(link) #Add to list to check
          found.append(link) #Add to master list of links found

          print('Match Found: ' + l)

      elif (raw_link not in rejected and link not in found):
        rejected.append(raw_link)

  pages_checked_counter = pages_checked_counter + 1
  print(pages_checked_counter, ' pages searched of ', len(page_list), ' pages found')

#Create the csv of links found DEPRECATED
with open(fileName,'a', newline='') as tempLog:

    header=['Link']
    csv.DictWriter(tempLog,header,delimiter=',', lineterminator='\n').writerows(found)
    print("Wrote to File "+fileName)

#Create the JSON of links found
with open(site_name + "/pages.json","w") as output:
  out = create_json(found)
  output.write(out)

#Create all the standardized logs
create_log(rejected, "rejected")
create_log(missing, "missing")
create_log(scripts, "assets")
create_log(images, "images")

#Create the site "package file" only after everything else has been successfully created
with open(site_name + "/info.json","w") as output:
  out = '{"path":"' + domain + '","created":"' + str(datetime.datetime.now()) + '"}'
  output.write(out)

print("All done!")