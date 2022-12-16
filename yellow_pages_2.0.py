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
      'Link':[],
      'Site':[],
      'Email':[]
      }

df = pd.DataFrame(df)

#scraping data

print(f"Please wait while the data is collected for {search_for.replace('+',' ')} in {city.title().replace('+',' ')}, {state.upper()}")

for pages in range(1,int(no_of_pages)+1): #for scraping data from multiple pages
    try: #if total pages entered are not available this will keep skipping the page and show an error
        print(f'Reading page no :{pages}')
        html_text = requests.get(f'https://www.yellowpages.com/search?search_terms={search_for}&geo_location_terms={city}%2C+{state}&page={pages}').text  #got the html text of listings page (1 by 1 page)
        print(f'Reading page {pages} done..')
        soup = BeautifulSoup(html_text, 'lxml')
        listings = soup.find('div', class_ = 'search-results organic').find_all('div', class_ = 'result')
        for index, listing in enumerate(listings): #for scraping data from multiple listings
            try:
                dealer_name = listings[index].div.div.find('div', class_ ='info').find('div', class_ ='info-section info-primary').h2.a.span.text  #collected business name
                dealer_phone = listings[index].div.div.find('div', class_ ='info').find('div', class_ ='info-section info-secondary').find('div', class_ = 'phones phone primary').text  #collected business phone
                dealer_street_address = listings[index].div.div.find('div', class_ ='info').find('div', class_ ='info-section info-secondary').find('div', class_ = 'adr').find('div', class_ = 'street-address').text  #collected street address
                dealer_locality = listings[index].div.div.find('div', class_ ='info').find('div', class_ ='info-section info-secondary').find('div', class_ = 'adr').find('div', class_ = 'locality').text  #collected locality
                dealer_link = listings[index].div.div.find('div', class_ ='info').find('div', class_ ='info-section info-primary').h2.a.get('href') #collected yellowpages.com link
                df.loc[len(df.index),['Name','Phone','Address','Link']] = [dealer_name, dealer_phone, f'{dealer_street_address}, {dealer_locality}',f'www.yellowpages.com{dealer_link}']  #entered the data in dataframe
                try: # website links and emails are not available in many cases that's why this 'try'
                    html_text2 = requests.get(f'http://www.yellowpages.com{dealer_link}').text
                    soup2 = BeautifulSoup(html_text2, 'lxml')
                    try: # if website link is found this will enter it into the row in which above data is entered
                        dealer_website = soup2.main.find('div', id='main-content').section.find('section', id='details-card').find('p',class_='website').a.text
                        df.loc[len(df.index)-1,'Site'] = dealer_website
                    except:
                        df.loc[len(df.index) - 1, 'Site'] = None
                    try: # if email is found this will enter it into the row in which above data is entered
                        dealer_email = soup2.main.find('div', id='main-content').section.find('section', id='business-info').dl.dd.a.get('href')
                        if '@' in dealer_email:  # sometimes data email is not available and some other text gets scraped, this eliminates that text
                            df.loc[len(df.index) - 1, 'Email'] = dealer_email
                    except:
                        df.loc[len(df.index) - 1, 'Email'] = None
                except: # if link to listing doesn't work this will show the given error
                    print("Couldn't collect email and website link.")
                print(f'{index + 1} Listings done')
            except: #if listing isn't scraped due to important missing details this error will show up
                print(f"Couldn't scrape listing {index+1} due to missing details.")
        if pages == 1: # to show which page has been scraped
            print(f'{pages} page done..........')
        else:
            print(f'{pages} pages done.............')
    except: # when there are no listings available on a page number, this error will show
        print("Page {pages} couldn't be scraped")

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
