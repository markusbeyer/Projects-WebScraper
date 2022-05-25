import requests #not necessary as html file is downloaded
import xlsxwriter #to write data to xlsx file
import re, time
from   bs4 import BeautifulSoup #for scraping all the data

#Scrapes names and emails addresses from HTML site I dont know the URL link of anymore
#and outputs it into a xsxx file in an ordered manner


PATH  = "cpgAdjustedFormated.html"
with open(PATH, "r", encoding="utf-8") as f:
     page = f.read()

soup   = BeautifulSoup(page, "html.parser")

names  = []
mails  = []
invids = []

investors = soup.select('a[target]')
emails    = soup.select('a[href^=mailto]')
ids       = soup.find_all('a')

for investor in investors:
     if "www" not in investor:
          print(investor.text)
          names.append(investor.text)

for email in emails:
     try:
          print(email.text)
          mails.append(email.text)
     except AttributeError:
          pass

for i in ids:
     if "www" not in str(i) and "@" not in str(i) and "http" not in str(i):
          cur_id = str(i.get("href")).strip("/profile/").strip("/person/profile").strip("/invest")
          print(cur_id)
          invids.append(cur_id)
          print("x")

print("Writing DATA now...")
time.sleep(1)
input("PRESS ENTER")

file      = xlsxwriter.Workbook("DATAFILE.xlsx")
worksheet = file.add_worksheet()#NOT ADD, WE NEED TO USE THE SHEET THATS THERE ALREADY

row = 2
col = 0

for data in invids:
    print(str(data))
    worksheet.write(row, col, str(data))
    row += 1

row = 2
col = 1

for data in names:
     print(str(data))
     worksheet.write(row, col, str(data))
     row += 1

row = 2
col = 2

for data in mails:
     print(str(data))
     worksheet.write(row, col, str(data))
     row += 1

worksheet.write(row, 0, 'Total')
worksheet.write(row, 1, '=SUM(B1:B4)')

file.close()

print("DONE!")
time.sleep(1)


#DIDNT WORK
#import scrapy
#
#class Parker(scrapy.Spider):
#     name       =  "JOB"
#     start_urls = ["/cpgAdjustedFormated.html"]
#
#     def parse(self, response):
#          SET_SELECTOR = "data-table__row data-table__row_fixed"
#          for i in response.css(SET_SELECTOR):
#               NAME_SELECTOR = "a ::text"
#               yield {
#                    "name": i.css(NAME_SELECTOR).extract_first(),
#                    }
#DIDNT WORK