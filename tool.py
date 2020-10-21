from bs4 import BeautifulSoup as BeautifulSoup
import requests
import csv
import certifi
import urllib3
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

domain = "https://rootree.ca"
debug_detection = False

# https://stackoverflow.com/questions/16208206/confused-by-python-file-mode-w

def functionA():
  
  fileName = "found-pages.csv"

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

  for link_object in page_list:
    url = link_object['Link']
    print('Searching: ',url)
    #page = requests.get(url)
    try:
      page = requests.get(url)
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
    
    # print(str(page))
    soup = BeautifulSoup(page.text, 'html.parser')

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
  
  with open("pages.json","w") as output:
    out = "["
    for obj in found:
      url = obj['Link']
      title=url.replace("/","")
      title=title.replace(".","dot")
      title=title.replace("?","query")
      title=title.replace("://","")
      out=out+'{"title":"' + title + '","address":"' + url + '"},'
    out=out[:-1] + ']'
    output.write(out)

  with open("rejected_log.txt",'w', newline='') as rejectedLog:
    for item in rejected:
      rejectedLog.write(item + "\n")
    print("Wrote to rejectedLog.txt")

  print("I'm Done! Take a look at the csv named "+fileName+"!")


def functionB():
  page_list2=[]
  with open('page_list.csv', 'r') as f_list:
    reader = csv.reader(f_list)
    page_list2 = list(reader)
    print(page_list2)
  




if __name__ == '__main__':
   functionA()
   #functionB()