from bs4 import BeautifulSoup as BeautifulSoup
import requests
import csv
import os
import certifi
import urllib3
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

domain = "https://darkcitycoffee.com"
site_name = "darkcity"

debug_detection = False

# https://stackoverflow.com/questions/16208206/confused-by-python-file-mode-w

def functionA():
  
  fileName = site_name + "-found-pages.csv"

  if not os.path.exists(site_name + '-cache'):
    os.makedirs(site_name + '-cache')

  page_list=[]
  page_list.append({"Link":domain})

  f = open(fileName, "w+")
  f.close()
  c=0
  i=0
  page=0
  fail=0

  # Find text objects
  found=[]
  rejected=[]
  missing=[]
  scripts=[]
  images=[]

  for link_object in page_list:
    url = link_object['Link']
    print('Searching: ',url)
    #page = requests.get(url)
    try:
      page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
      #page = http.request('GET', url)
      fail=0
    except:
      fail=fail+1
      print('Request Failed ', fail)
      if(fail>10):
        print('Giving Up')
        break
      else:
        page_list.append({"Link":url})
        continue
    
    if (page.status_code != 200):
      missing.append(url + " returned code " + str(page.status_code))
    
    soup = BeautifulSoup(page.text, 'html.parser')

    cache_path = site_name + "-cache/" + create_title(url) + ".dat"

    with open(cache_path, "w") as cache_file:
      cache_file.write(url + "\n----\n" + page.text)

    for a in soup.find_all('script', src=True):
      if not a['src'] in scripts:
        scripts.append(a['src'])

    for a in soup.find_all('img', src=True):
      if not a['src'] in images:
        images.append(a['src'])
    
    for a in soup.find_all('a', href=True):
      #print(url +": "+ a['href']) 
      l = a['href']

      if l:

        link_in_scope = (domain in l or l[0] == "/" or not "http" in l)
        link_not_an_anchor = l[0] != "#"
        link_valid_type = not ".png" in l and not ".jpg" in l and not ".pdf" in l and not ".webp" in l and not ".svg" in l and not "tel:" in l and not "javascript:void" in l and not "mailto:" in l and not "fax:" in l and not "ts3server:" in l and not "callto:" in l
        link_not_excluded_dir = not "/uploads/" in l

        raw_link = l

        if(debug_detection):
          print(l)
          print(link_in_scope)
          print(link_not_an_anchor)
          print(link_valid_type)
          print(link_not_excluded_dir)

        if not domain in l:
          if(l[0] != "/"):
            l = "/" + l
          link = {'Link':domain + l}
        else:
          link = {'Link':l}

        if link_not_an_anchor and link_in_scope and link_valid_type and link_not_excluded_dir and not link in found:
            
            page_list.append(link)
            found.append(link)

            c=c+1
            print('Match Found: ' + l)
        elif (raw_link not in rejected and link not in found):
          rejected.append(raw_link)

    i=i+1
    print(i, ' pages searched of ', len(page_list), ' pages found')

  with open(fileName,'a', newline='') as tempLog:
      header=['Link']
      csv.DictWriter(tempLog,header,delimiter=',', lineterminator='\n').writerows(found)
      print("Wrote to File "+fileName)
  
  with open(site_name + "-pages.json","w") as output:
    out = create_json(found)
    output.write(out)

  create_log(rejected, "rejected")
  create_log(missing, "missing")
  create_log(scripts, "assets")

def create_json(found):
  out = "["
  for obj in found:
    url = obj['Link']
    title = create_title(url)
    out=out+'{"title":"' + title + '","address":"' + url + '"},'
  out=out[:-1] + ']'
  return out

def create_log(file_list, name):
  with open(site_name + "-" + name + "_log.txt",'w', newline='') as rejectedLog:
    for item in file_list:
      rejectedLog.write(item + "\n")
    print("Wrote to " + site_name  + "-" + name + "_log.txt")

def create_title(url):
  title=url.replace("/","")
  title=title.replace(".","dot")
  title=title.replace("?","query")
  title=title.replace(":","")
  return title

if __name__ == '__main__':
   functionA()