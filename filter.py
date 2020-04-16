import csv
import re

tofilter=[]
out=''

with open('find-a.csv', 'r') as f_list:
    reader = csv.reader(f_list)
    out='['
    for url in reader:
        url=url[0]
        
        if(re.search('\d{7,10}$',url)):
            url=url.replace('/inventory/v1/Current/','')
            url=url.replace('/',',')
            url=url.replace('-',' ')
            url=url.replace('  Stouffville Ontario   ',',')
            url=url.replace('Farm Equipment,','')
            listing=url.split(',')
            trimid=listing[len(listing)-1]
            modeltrim=listing[len(listing)-2]
            #print(listing)
            out=out+'{"trimid":' + trimid + ',"modeltrim":"'+modeltrim + '"},'
out=out[:-1] + ']'
#print(out)
with open('trims.json', 'w') as f_list:
    f_list.write(out)
print('Done!')