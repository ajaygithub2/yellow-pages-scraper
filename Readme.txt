Through this script you will be able to scrape Name, Contact, Address and Link to the yellowpages page.

When the script starts, it will ask for 5 inputs:

Looking for : [Enter what you are looking for, like : doctors, dermatologist, bike repair, insurance, lawyer, accountant etc.]
City : [City you want data for]
State : [Please enter only in abbreviation like TX or ME or CA etc.]
No of pages to scrape : [Per page includes approx 30 records so if you enter 3 you will get around 90 records]
Data Format : [Enter 1 for csv, 2 for xlsx, 3 for pdf]

Note: CSV format is recommended.
Note: If you get less records, that means that more records aren't available on the site.


Install these libraries:

1. Pandas : pip install pandas OR 
            conda install pandas

2. Pdfkit : pip install pdfkit OR
            conda install -c conda-forge python-pdfkit

3. BeautifulSoup : pip install bs4 OR
                   conda install -c conda-forge bs4

4. Requests : python -m pip install requests OR
              conda install -c anaconda requests


Note: If you want your output in a pdf file, you will have to install an additional library called 'wkhtmltopdf',
      if not, then there is no need to install it.

Run the script and enjoy. Thankyou.


Yellow_pages_2.0.py :

This is an updated version of 'yellowpages.py'.
Updates:
1. Scrapes emails and websites
2. Shows status of pages scraped and listings scraped in those pages.
3. Doesn't skip a page if a listing has missing info. (Only skips the listing)

These updates involves reading one webpage per listing which makes it slower then previous version. 
So if you don't need these 2 , I recommend using the previous version.

Thankyou.
