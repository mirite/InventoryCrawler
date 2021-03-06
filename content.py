########
# Imports
#######
import json

#File/operating system related imports
import os
import sys
import re

import os.path
from os import path

#Network request related imports
import certifi
import requests
import urllib3
import urllib

from bs4 import BeautifulSoup as BeautifulSoup #Used for page navigation

########
# Helper Functions
#######

#Remove unwanted attributes from parent tag
def strip_meta(a):
  del a['class']
  del a['style']
  del a['id']
  del a['data-region']
  del a['data-shogun-id']
  del a['data-shogun-page-id']
  del a['data-shogun-page-version-id']
  del a['data-shogun-platform-type']
  del a['data-shogun-site-id']
  del a['data-shogun-variant-id']
  del a['data-col-grid-mode-on']
  del a['data-shg-href-target']
  del a['height']
  del a['width']
  del a['data-bgset']
  del a['contenteditable']
  if "href" in a:
    a['href'] = "intentional404.php"

#Remove divs and pretty up the html for writing
def strip_structure(html):
  
  content = re.sub(r"<\/?div[A-Za-z\=\"\'\d\ \-]*>","",html)
  content = re.sub(r"<\/?span[A-Za-z\=\"\'\d\ \-]*>","",content)
  content = re.sub(r"<\/?meta[A-Za-z\=\"\'\d\ \-]*>","",content)
  content = re.sub(r"[\n\r\t\u000A]*","",content)
  content = re.sub(r"\ +"," ",content)
  # content = html.replace("<div>","")
  # content = content.replace("</div>","")
  # content = content.replace("<span>","")
  # content = content.replace("</span>","")
  #content = ' '.join(content.split()) #get rid of excess white space
  return content

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
image_index = 1
saved_html_bytes = 0
saved_content_bytes = 0
info_file = []

########
# Main body
#######


print("\n##########\n# Rootree Shogun Tool\n##########")

#Load the site info from the crawler
config = load_config(site_name)
pages = get_pages(config)

print("Converting pages from",config['path'],"crawled on",config['created'],"\n")

base_path = site_name + '/converted/'
if not os.path.exists(base_path):
  os.makedirs(base_path)

#Loop through all pages
for page in pages:

  try:
    cache_path = site_name + "/cache/" + page['title'].replace("â€“","") + ".dat"
    with open(cache_path, "r", encoding="utf-8") as cache_file:

        content = cache_file.read()
        content = content.replace('style=""',"")
        content = content.replace("\n","")
        content = content.replace("data-src","src")

        soup = BeautifulSoup(content, 'html.parser')

        real_title = soup.title.string

        passes = 0 #Right now I'm doing three passes with no changes
        
        #Only deal with pages with shogun content
        for a in soup.find_all("main"):

          initial_size = len(a.prettify(formatter="minimal"))

          title = page['title']
          title = title.replace("httpsrootreedotca","") #fix hardcode value
          if(title == ""):
            title = "no_title"
          
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
              inner_content = str(d.text).strip()
              inner_content = inner_content.replace("\n","")
              inner_content = inner_content.replace(" ","")

              if(len(list(d.findChildren())) == 0 and len(inner_content) == 0):
                d.extract()
                changes = changes + 1
              elif(child_count == 1):
                d.unwrap()
                #print(str(d.children))
                #d.replace_with(list(d.children)[0])
                changes = changes + 1
                singles = singles + 1

            for s in a('span'):
              strip_meta(s)
              if(len(s.contents) == 0 or len(str(s.string).strip()) == 0):
                s.extract()
                changes = changes + 1
            
            for p in a('p'):
              strip_meta(p)
            
          total_changes = total_changes + changes

          relative_path = page["address"].replace(config["path"],"")

          if(relative_path[0] == "/"):
              relative_path = relative_path[1:]

          print(relative_path)
          
          if(len(relative_path) > 1 and "/" in relative_path):

            if(relative_path[len(relative_path)-1]) == "/":
              relative_path = relative_path[0:len(relative_path)-1]

            split_path = relative_path.rsplit("/",1)
            file_name = split_path[1]
            relative_path = split_path [0] + "/"
            
            if not ".html" in file_name:
              file_name = file_name + ".html"

          else:
              file_name = "index.html"
              relative_path = ""
          
          converted_path = base_path + relative_path + file_name.replace(".html","_o.html")
          content_path = base_path + relative_path + file_name

          image_path = base_path + relative_path + "images"
          print(converted_path, content_path, image_path)
          
          if not os.path.exists(image_path):
            os.makedirs(image_path)

          for i in a.find_all('img'):
            if(i.has_attr('src')):
              try:
                src = i['src']

                if(src[0:2] == "//"):
                  src = "https:" + src

                split_src = src.split(".")
                #file_type = "." + split_src[len(split_src)-1]
                file_type = ".jpg"
                new_path = image_path + "/image_" + str(image_index) + file_type
                urllib.request.urlretrieve(src, new_path)
                i['src'] = "images/" + "image_" + str(image_index) + file_type
                image_index = image_index + 1
              except Exception as e:
                print("Error processing image",i,e)
              

          html = a.prettify(formatter="minimal")

          final_html_size = len(html)
          saved_html_bytes = saved_html_bytes + (initial_size - final_html_size)

          bscontent = BeautifulSoup(strip_structure(html), 'html.parser')

          for s in bscontent('a'):
            strip_meta(s)

          for s in bscontent('img'):
            strip_meta(s)

          for s in bscontent('h2'):
            strip_meta(s)
          
          for s in bscontent('span'):
            strip_meta(s)
          
          for s in bscontent('li'):
            strip_meta(s)
          
          for s in bscontent('aside'):
            strip_meta(s)
          
          for s in bscontent('nav'):
            strip_meta(s)

          content = strip_structure(str(bscontent))
          final_content_size = len(content)
          saved_content_bytes = saved_content_bytes + (initial_size - final_content_size)

          with open(converted_path,"w", encoding="utf-8") as output:
            output.write(html)

          with open(content_path,"w", encoding="utf-8") as output:
            output.write(content)
          
          content_type = ""

          if "blogs" in content_path:
            content_type = "blog"
          elif "pages" in content_path:
            content_type = "page"
          else:
            content_type = "other"

          info_file.append({"title":real_title,"content_type":content_type,"content_path":content_path,"media": base_path + "/images"})
          print("Start:",initial_size,"Structure:",final_html_size,"Content:",final_content_size)

    #break #Uncomment to test only first file for debug
  except Exception as e:
    print("Error processing",page['title'],e)
  

print("\nDone!", str(total_changes), "change made.", str(singles), "single child divs eliminated.\n",saved_html_bytes,"bytes saved with structure.",saved_content_bytes,"bytes saved with content only.\n")

with open(site_name + "/converted/converted.json","w") as w:
  w.write(json.dumps(info_file))
  print("Wrote JSON")