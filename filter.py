import csv
import re

tofilter=[]

with open('find-a.csv', 'r') as f_list:
    reader = csv.reader(f_list)

    for url in reader:
        url=url[0]
        if(re.search('\d{5,10}$',url)):
            url=url.replace('/inventory/v1/Current/','')
            url=url.replace('/',',')
            url=url.replace('-',' ')
            url=url.replace('  Stouffville Ontario   ',',')
            url=url.replace('Farm Equipment,','')
            print(url)