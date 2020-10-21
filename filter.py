import csv
import re

tofilter=[]
out=''

with open('find-a.csv', 'r') as f_list:
    reader = csv.reader(f_list)
    out='['
    for url in reader:
        url=url[0]
        
        #if(re.search(r'\d{7,10}$',url)):
        #url=url.replace('rootree.ca/','')
        #url=url.replace('https://','')
        #url=url.replace('/',',')
        #url=url.replace('-',' ')
        #url=url.replace('  Stouffville Ontario   ',',')
        #url=url.replace('Farm Equipment,','')
        #listing=url.split(',')
        #trimid=listing[len(listing)-1]
        #modeltrim=listing[len(listing)-2]
        #print(listing)
        if url!="":
            if(url[0]=="/"):
                url=url[1:int(len(url))]
            title=url.replace("/","")
            title=title.replace(".","dot")
            title=title.replace("?","query")
            title=title.replace("://","")
            out=out+'{"title":"' + title + '","address":"' + url + '"},'

out=out[:-1] + ']'
#print(out)
with open('trims.json', 'w') as f_list:
    f_list.write(out)
print('Done!')