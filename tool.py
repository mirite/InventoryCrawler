from bs4 import BeautifulSoup as BeautifulSoup
import requests
import csv

# https://stackoverflow.com/questions/16208206/confused-by-python-file-mode-w

search = "a"
fileName = "find-"+search+".csv"

# with open('allPages.csv', 'r') as f_list:
#   reader = csv.reader(f_list)
#   page_list = list(reader)
#   print(page_list)
page_list=[]
page_list.append("https://www.hutchinsonfarmsupply.ca/inventory/v1/")

f = open(fileName, "w+")
f.close()

with open(fileName,'a') as tempLog:
    csv.writer(tempLog).writerow(["Title","Links"])

def sanitize(this):
  # SPECIFIC STRINGS
  # this = str(this).replace('<a href="https://www.google.com/maps/dir//43.6492216, -79.3807795/@43.649222, -79.38078, 16z?hl=en-US">','').replace('<div class="col-xs-12 col-sm-4 col-md-2" id="branch-contact">','').replace('<i aria-hidden="true" class="fa fa-phone hidden-md"></i>','').replace('<i aria-hidden="true" class="fa fa-envelope hidden-md"></i>','').replace('<p class="medium">','').replace('<ul class="medium list-unstyled">','').replace('<div class="col-xs-12 col-sm-4 col-md-3" id="branch-hours">','').replace('<a href="tel:','').replace('<a href="mailto:',', ').replace('" onclick="ga(',', ').replace('<div class="pull-left">','').replace('<div class="pull-left','').replace('<p class="medium canadian','').replace('Canadian Owned and Operated','').replace("I'm ",'').replace('TPH<sup>®</sup>','').replace('your ','').replace('<img alt="','').replace('" class="pull-left" src="',': ').replace('Manager.','Manager').replace('<span style=""letter-spacing: -1px;', '').replace('<a href="https://www.google.com/maps/dir//43.6492216,-79.3807795/@43.649222,-79.38078,16z?hl=en-US">','').replace('<img "="" alt="','').replace('<span style="letter-spacing: -1px;, ','').replace('<span ','').replace('style="letter-spacing:','')
 
  # BROAD STRINGS
  # this = str(this).replace('\n', ' ').replace('\r', '').replace('[ ', '').replace('[', '').replace(']', '').replace(',',', ').replace('">',', ').replace('"/>','').replace('	','').replace('  ',' ').replace('   ',' ').replace('    ',' ').replace('   ',' ').replace('<br/>',', ').replace('<p class="medium">','').replace('<p>','').replace('</p>','').replace('<span style="letter-spacing: -1px;">','').replace('<span style="letter-spacing:-1px">','').replace('</span>','').replace('</a>','').replace('<strong>','').replace('</strong>','').replace('<li>','').replace('</li>','').replace('<div>','').replace('</div>','').replace('<ul>','').replace('</ul>','').replace('<b>','').replace('</b>','').replace('<small>','').replace('</small>','').replace(' , ','').replace('  ',' ').replace('-1px, ','').replace('-1px;, ','')
  return this

#.replace('','')
#.replace('" onclick="ga(\'send\', \'event\', { eventCategory: \'Call-to-branch\', eventAction: \'Phone-click\', eventLabel: \'/call-to-branch\'});',', ')

# Find text objects

for x in page_list:
  url = x
  page = requests.get(url)
  links = []
  # print(str(page))
  soup = BeautifulSoup(page.text, 'html.parser')

  # <p class="medium canadian">Canadian Owned and Operated</p>
  # pull_instance = soup.select(search)
  title=soup.find('title').contents[0]
  for a in soup.find_all('a', href=True):
    print(url +": "+ a['href']) 
    links.append("https://www.hutchinsonfarmsupply.ca" + a['href'])
  # pull_instance = soup.find_all("iframe", src=True)
  # pull_string = str(pull_instance)
  # print(url +": "+ pull_string)
  # pull_hours = soup.select('#branch-hours')
  # pull_phone = soup.select('#branch-contact a strong')
  # pull_phone = pull_phone + soup.select('#branch-contact a b')
  # pull_address = soup.select('#branch-address p')
  # pull_manager_imgsrc = soup.select('#branch-manager img')
  # pull_manager_info = soup.select('#branch-manager div')
  # pull_email = str('branch'+x+'@tph.ca')
  # print(x+": "+sanitize(pull_address))
  # print(x+": "+sanitize(pull_phone))
  # print(x+": "+sanitize(pull_email))
  # print(x+": "+sanitize(pull_manager_imgsrc))
  # print(x+": "+sanitize(pull_manager_info))
    
  # print("------------------------------------------------")

  # Write out to file
  # branch = x
  # address = sanitize(pull_address)
  # phone = sanitize(pull_phone)
  # email = sanitize(pull_email)
  # hours = sanitize(pull_hours)
  # managerimg = sanitize(pull_manager_imgsrc)
  # managerinfo = sanitize(pull_manager_info)
  # found = pull_string

  with open(fileName,'a') as tempLog:
    # csv.writer(tempLog).writerow([branch, address, phone, email, managerimg, managerinfo, hours])
    for l in links:
      if l.startswith('\/inventory\/v1\/Current\/'):
        csv.writer(tempLog, delimiter=',', escapechar=' ', quoting=csv.QUOTE_NONE).writerow([title, l])
        print('Match Found: ' + l)
    print("Wrote to File "+fileName)
    #csv.writer(tempLog).writerow([" ", "", "", ""])

print("I'm Done! Take a look at the csv named "+fileName+"!")