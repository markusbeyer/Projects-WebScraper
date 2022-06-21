import requests
import time
from bs4                    import BeautifulSoup
from forex_python.converter import CurrencyRates

#Has to scrape from target website (https://www.peopleperhour.com/services/guest+post?page=%s&ref=search):
#URLs of gigs
list_of_links   = []
#Titles of gigs
list_of_titles  = []
#Prices of gig
list_of_prices  = []
#Delivery time
list_of_dtime   = []
#Rating
list_of_rating  = []
#Reviews
list_of_reviews = []
#Response Time
list_of_rtime   = []

#var for converting EUR to USD
c = CurrencyRates()

#get maximum page number
page = requests.get("https://www.peopleperhour.com/services/guest+post?page=%s&ref=search" %1)
soup = BeautifulSoup(page.text, "html.parser")
items = soup.find_all('a', class_="pagination__link⤍SimplePagination⤚1MYH2")
pagenumbers = []
for item in items:
    if item.text != "":
        pagenumbers.append(int(item.text))
max  = int(max(pagenumbers))+1#plus one, because range(0,max) gets everything in BETWEEN
maxp = max-1
    

# Get all of the links to each blog post

for page_number in range(0, max):
    page = requests.get("https://www.peopleperhour.com/services/guest+post?page=%s&ref=search" %page_number) #search results (25 gigs)
    soup = BeautifulSoup(page.text, "html.parser")
    print("----------------------------------")
    print("PAGE "+str(page_number)+"/"+str(maxp)) #current page
    print("----------------------------------")
    list_of_links.append( "PAGE " +str(page_number)+"/"+str(maxp))
    list_of_titles.append("PAGE " +str(page_number)+"/"+str(maxp))
    list_of_prices.append("PAGE " +str(page_number)+"/"+str(maxp))
    list_of_dtime.append("PAGE "  +str(page_number)+"/"+str(maxp))
    list_of_rating.append("PAGE " +str(page_number)+"/"+str(maxp))
    list_of_rtime.append("PAGE "  +str(page_number)+"/"+str(maxp))
    list_of_reviews.append("PAGE "+str(page_number)+"/"+str(maxp))
    items = soup.find_all('ul', class_="list⤍ResultsList⤚21s3j list--mgb-0⤍ResultsList⤚3qxNR")
    for item in items: #going through 25 gigs
        print(item)
        print("\n")
        title = item.find("h2",class_="title-nano card__title⤍HourlieTile⤚5LQtW")
        title = str(title.text)
        print("TITLE         : "+title)
        print("LINK          : "+item.find('a')['href'])
        price = item.find("div",class_="u-txt--right card__price⤍HourlieTileMeta⤚3su1s")
        price = str(price.text)
        print("PRICE         : "+price)
        list_of_titles.append(title)
        list_of_links.append(item.find('a')['href'])
        list_of_prices.append(price)
        link = str(item.find('a')['href']) # link to current gig
        page2 = requests.get(link) # current gig
        soup2 = BeautifulSoup(page2.text, "html.parser")
        maininfo = soup2.find_all('div', class_="clearfix main-information row")
        first = True
        for i in maininfo: # getting more info of current gig
            if first == True:
                stuff         = i.find_all('span')
                try:
                    deliver_in    = str(stuff[0].text).strip("\n")
                    print("DELIVERY IN   : "+deliver_in)
                except IndexError:
                    deliver_in    = "NO DELIVERY TIME FOUND"
                    print("NO DELIVERY TIME FOUND")
                try:
                    rating        = str(stuff[1].text).strip("\n")
                    print("RATING        : "+rating)
                except IndexError:
                    rating        = "NO RATINGS FOUND"
                    print("NO RATINGS FOUND")
                try:
                    reviews = str(stuff[2].text).strip("\n")
                    print("REVIEWS       : "+reviews)
                except IndexError:
                    response_time = "NO REVIEWS FOUND"
                    print("NO REVIEWS FOUND")
                try:
                    response_time = str(stuff[3].text).strip("\n")
                    print("RESPONSE TIME : "+response_time)
                except IndexError:
                    response_time = "NO RESPONSE TIME FOUND"
                    print("NO RESPONSE TIME FOUND")
                list_of_dtime.append(deliver_in)
                list_of_rating.append(rating)
                list_of_rtime.append(response_time)
                list_of_reviews.append(reviews)
                first = False
            elif first == False:
                first = True

with open('list_TITLES.txt', 'w+') as f:
    for line in list_of_titles:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('list_URLS.txt', 'w+') as f:
    for line in list_of_links:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('list_PRICES.txt', 'w+') as f:
    for line in list_of_prices:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('list_DTIMES.txt', 'w+') as f:
    for line in list_of_dtime:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('list_RATINGS.txt', 'w+') as f:
    for line in list_of_rating:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('list_RTIMES.txt', 'w+') as f:
    for line in list_of_rtime:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('list_REVIEWS.txt', 'w+') as f:
    for line in list_of_reviews:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

zipped = zip(list_of_titles, list_of_links, list_of_prices, list_of_dtime, list_of_rating, list_of_rtime, list_of_reviews)
with open("DATA.txt","w+") as f:
    for data in zipped:
        f.write(str(str(data).encode("utf8")) + "\n")
    f.close()

print("DONE")
