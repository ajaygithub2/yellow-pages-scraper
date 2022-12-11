#!/usr/bin/env python
# coding: utf-8

# importing required libraries

import requests
from bs4 import BeautifulSoup
import pandas as pd
import pdfkit

# inputs

search_for = input('Looking for : ').replace(' ','+')
city = input('City : ').replace(' ','+')
state = input("State (abbreviation) : " )
no_of_pages = input('No of pages to scrape : ')
data_format = input('Press and enter \n1 for csv (recommended)\n2 for xlsx\n3 for pdf : ')


#creating dataframe

df = {'Name':[],
      'Phone':[],
      'Address':[],
      'Link':[]
     }

df = pd.DataFrame(df)

#scraping data

print(f"Please wait while the data is collected for {search_for.replace('+',' ')} in {city.title().replace('+',' ')}, {state.upper()}")

for pages in range(1,int(no_of_pages)+1):
    try:
      html_text = requests.get(f'https://www.yellowpages.com/search?search_terms={search_for}&geo_location_terms={city}%2C+{state}&page={pages}').text
      soup = BeautifulSoup(html_text, 'lxml')
      listings = soup.find('div', class_ = 'search-results organic').find_all('div', class_ = 'result')
      for index, listing in enumerate(listings):
          try:
              dealer_name = listings[index].div.div.find('div', class_ ='info').find('div', class_ ='info-section info-primary').h2.a.span.text
              dealer_phone = listings[index].div.div.find('div', class_ ='info').find('div', class_ ='info-section info-secondary').find('div', class_ = 'phones phone primary').text
              dealer_street_address = listings[index].div.div.find('div', class_ ='info').find('div', class_ ='info-section info-secondary').find('div', class_ = 'adr').find('div', class_ = 'street-address').text
              dealer_locality = listings[index].div.div.find('div', class_ ='info').find('div', class_ ='info-section info-secondary').find('div', class_ = 'adr').find('div', class_ = 'locality').text
              dealer_link = listings[index].div.div.find('div', class_ ='info').find('div', class_ ='info-section info-primary').h2.a.get('href')
              
              df.loc[len(df.index)] = [dealer_name, dealer_phone, f'{dealer_street_address}, {dealer_locality}',f'www.yellowpages.com{dealer_link}']
                  
          except:
              pass
      if pages == 1:
          print(f'{pages} page done...')
      else:
          print(f'{pages} pages done...')
     except:
      pass

#converting to required format
print('Creating your file...')

if data_format == str(1):
    df.to_csv(f"{search_for.replace('+','_')}_{city.replace('+','_')}.csv", index = False)
elif data_format == str(2):
    df.to_excel(f"{search_for.replace('+','_')}_{city.replace('+','_')}.xlsx")
else:
    f = open(f'{search_for}.html','w')
    a = df.to_html()
    f.write(a)
    f.close()
    
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_file(f'{search_for}.html', f"{search_for.replace('+','_')}_{city.replace('+','_')}.pdf", configuration=config)
    
print('Done. You can now access the file in your local directory.')

