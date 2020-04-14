from bs4 import BeautifulSoup as BeautifulSoup
import requests
import csv

# https://stackoverflow.com/questions/16208206/confused-by-python-file-mode-w

def functionA():
  search = "a"
  fileName = "find-"+search+".csv"

  page_list=[]
  page_list.append("https://www.hutchinsonfarmsupply.ca/inventory/v1/")
  #page_list.append('https://www.hutchinsonfarmsupply.ca/inventory/v1/Current/John-Deere/Tillage/Rippers')

  f = open(fileName, "w+")
  f.close()
  c=0
  i=0
  page=0
  # Find text objects
  found=[]
  for url in page_list:
    print('Searching: ',url)
    try:
      page = requests.get(url)
    except:
      print('Request Failed')
      break
      #print(found)
      #break
    
    # print(str(page))
    soup = BeautifulSoup(page.text, 'html.parser')

    title=soup.find('title').contents[0]
    

    for a in soup.find_all('a', href=True):
      #print(url +": "+ a['href']) 
      l=a['href']
      link={'Title':title,'Link':l}
      if l.startswith('/inventory/') and not link in found:
          found.append(link)
          page_list.append('https://www.hutchinsonfarmsupply.ca' + l)
          c=c+1
          print('Match Found: ' + l)
          print(c, ' Matches')
    i=i+1
    print(i, ' pages searched, ', len(page_list), ' in queue')

  with open(fileName,'a', newline='') as tempLog:
      header=['Title','Link']
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