import pandas as pd
from bs4 import BeautifulSoup
import requests

search = input('Looking for: ').replace(' ','+')
no_of_pages = input('Pages to be scraped: ')
city = input('City:').replace(' ','+')

info = pd.DataFrame()

for pages in range(1,int(no_of_pages)+1):
    html_text = requests.get(f'https://www.yellowpages.com/search?search_terms={search}&geo_location_terms={city}%2C+CA&page={pages}').text
    soup = BeautifulSoup(html_text, 'lxml')
    listings = soup.find('div', class_='search-results organic').find_all('div', class_='result')
    for index, value in enumerate(listings):
        try:
            business_name = listings[index].div.div.find('div', class_ = 'info').find('div', class_ ='info-section info-primary').h2.a.span.text
            business_contact = listings[index].div.div.find('div', class_ = 'info').find('div', class_ ='info-section info-secondary').find('div', class_ = 'phones phone primary').text
            business_street = listings[index].div.div.find('div', class_ = 'info').find('div', class_ ='info-section info-secondary').find('div', class_ = 'adr').find('div', class_ = 'street-address').text
            business_locality = listings[index].div.div.find('div', class_ = 'info').find('div', class_ ='info-section info-secondary').find('div', class_ = 'adr').find('div', class_ = 'locality').text
            business_link = listings[index].div.div.find('div', class_ = 'info').find('div', class_ ='info-section info-primary').h2.a.get('href')
            print(f'Name: {business_name}\nContact: {business_contact}\nAddress: {business_street}, {business_locality}\nLink: www.yellowpages.com{business_link}')
            info.loc[len(info),['Name', 'Contact', 'Address', 'Link']] = [business_name, business_contact, f'{business_street},{business_locality}', f'www.yellowpages.com{business_link}']
        except:
            pass

info.to_csv(f'{search}.csv')