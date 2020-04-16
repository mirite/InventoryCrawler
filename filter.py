import csv
import re

tofilter=[]

with open('find-a.csv', 'r') as f_list:
    reader = csv.reader(f_list)

    for url in reader:
        if(re.search('\d{5,10}$',url[0])):
            print(url[0])