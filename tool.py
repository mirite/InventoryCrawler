from bs4 import BeautifulSoup as BeautifulSoup
import requests
import csv

# https://stackoverflow.com/questions/16208206/confused-by-python-file-mode-w

def functionA():
  search = "a"
  fileName = "find-"+search+".csv"

  page_list=[]
  page_list.append("https://darkcitycoffee.local/")
  #page_list.append('https://www.hutchinsonfarmsupply.ca/inventory/v1/Current/John-Deere/Tillage/Rippers')

  f = open(fileName, "w+")
  f.close()
  c=0
  i=0
  page=0
  fail=0

  # Find text objects
  found=[]
  for url in page_list:
    print('Searching: ',url)
    #page = requests.get(url)
    try:
      page = requests.get(url, verify=False)
      fail=0
    except:
      fail=fail+1
      print('Request Failed ', fail)
      if(fail>10):
        print('Giving Up')
        break
      else:
        page_list.append(url)
        continue
    
    # print(str(page))
    soup = BeautifulSoup(page.text, 'html.parser')

    for a in soup.find_all('a', href=True):
      #print(url +": "+ a['href']) 
      l=a['href']
      link={'Link':l}
      if l[0] != "#" and ("https://darkcitycoffee.local" in l or l[0] == "/") and not ".png" in l and not ".jpg" in l and not "/product/" in l and not "/product-category/" in l and not "/uploads/" in l and not '?' in l and not link in found:
          
          
          found.append(link)
          if "https://darkcitycoffee.local" in l:
            page_list.append(l)
          else:
            page_list.append('http://darkcitycoffee.local' + l)
          
          c=c+1
          print('Match Found: ' + l)
    i=i+1
    print(i, ' pages searched of ', len(page_list), ' pages found')

  with open(fileName,'a', newline='') as tempLog:
      header=['Link']
      csv.DictWriter(tempLog,header,delimiter=',', lineterminator='\n').writerows(found)
      print("Wrote to File "+fileName)

  print("I'm Done! Take a look at the csv named "+fileName+"!")


def functionB():
  page_list2=[]
  with open('find-a.csv', 'r') as f_list:
    reader = csv.reader(f_list)
    page_list2 = list(reader)
    print(page_list2)



if __name__ == '__main__':
   functionA()
   #functionB()