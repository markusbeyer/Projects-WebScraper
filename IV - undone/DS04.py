import requests, time, xlsxwriter, chromedriver_autoinstaller
from bs4                               import BeautifulSoup
from forex_python.converter            import CurrencyRates
from selenium.webdriver.common.by      import By
from statistics                        import mode
from selenium                          import webdriver
from selenium.common.exceptions        import NoSuchElementException
from selenium.webdriver.common.keys    import Keys
from selenium.webdriver                import ActionChains

#### TO SCRAPE
#
#Name
item_name = []
#Preis
item_price = []
#Bewertung
item_ratings = []
#Farben
item_colors = []

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
driver.get("https://www.wayfair.com/furniture/sb0/coffee-tables-c414602.html?prefetch=true")
driver.maximize_window()
time.sleep(2)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
print("[*] Scrolled down.")
time.sleep(2)
element = driver.find_element(By.XPATH, '//*[@id="sbprodgrid"]/div[3]/div/nav/span[4]')
maxpage = int(str(element.text).strip(" "))
nowpage = 0
print("[*] Search has "+str(maxpage)+" pages.")

mainloop = True
while mainloop == True:
    nowpage += 1
    if nowpage == (maxpage):
        mainloop = False
    print("Page "+str(nowpage)+"/"+str(maxpage))
    end = nowpage
    url = "https://www.wayfair.com/furniture/sb0/coffee-tables-c414602.html?curpage="+str(end)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    itemloop = True
    while itemloop == True:
        html  = driver.page_source
        soup  = BeautifulSoup(html, "html.parser")
        items = soup.find_all('a', {"data-codeception-id" :"BrowseProductCard-wrapper"})
        if str(items) == "[]":
            print("ITEMS EMPTY.")
            if "captcha_status" in str(driver.current_url):
                print("CAPTCHA REQUIRED.")
                input("PRESS ENTER WHEN DONE")
                print("PROCEEDING...")
        else:
            itemloop = False
    y     = 0
    for item in items:
        y += 1
    x     = 0
    for item in items:
        #time.sleep(0.5)
        x += 1
        area = ""
        print("Item "+str(x)+"/"+str(y))
        print("\n")
        try:
            print("NAME                  : "+str(item.find('h2', class_="ProductCard-name").text))
            item_name.append(str(item.find('h2', class_="ProductCard-name").text))
        except AttributeError:
            try:
                print("NAME                  : "+str(item.find('h2', class_="ProductCard-name").text))
                item_name.append(str(item.find('h2', class_="ProductCard-name").text))
            except AttributeError:
                print("NO NAME FOUND         : NO NAME FOUND")
                item_name.append("NONE FOUND")
        try:
            print("PRICE                 : "+str(item.find('span', class_="ProductCard-price ProductCard-price--sale").text))
            item_price.append(str(item.find('span', class_="ProductCard-price ProductCard-price--sale").text))

        except AttributeError:
            try:
                print("PRICE                 : "+str(item.find('span', class_="ProductCard-price").text))
                item_price.append(str(item.find('span', class_="ProductCard-price").text))
            except AttributeError:
                print("NO PRICE FOUND        : NO PRICE FOUND")
                item_price.append("NO PRICE FOUND        : NO PRICE FOUND")
        try:
            print("RATINGS               : "+str(item.find('p', class_="pl-ReviewStars-reviews").text))
            item_ratings.append(str(item.find('p', class_="pl-ReviewStars-reviews").text))
        except AttributeError:
            print("NO RATINGS FOUND      : NO RATINGS FOUND")
            item_ratings.append("NO RATINGS FOUND      : NO RATINGS FOUND")
        try:
            print("COLORS                : "+str(item.find('span', {"aria-hidden" :"true"}).text))
            item_colors.append(str(item.find('span', {"aria-hidden" :"true"}).text))
        except AttributeError:
            print("NO COLORS FOUND       : NO COLORS FOUND")
            item_colors.append("NO COLORS FOUND       : NO COLORS FOUND")
        print("_____________________________________________________________")
driver.quit()

item_name.insert(   0,"ITEM NAMES")
item_price.insert(  0,"ITEM PRICE")
item_ratings.insert(0,"ITEM RATINGS")
item_colors.insert( 0,"ITEM COLORS")

zipped = zip(item_name,item_price,item_ratings,item_colors)

with open('item_name.txt', 'w+') as f:
    for line in item_name:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('item_price.txt', 'w+') as f:
    for line in item_price:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('item_ratings.txt', 'w+') as f:
    for line in item_ratings:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('item_colors.txt', 'w+') as f:
    for line in item_colors:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open("DATA.txt","w+") as f:
    for data in zipped:
        f.write(str(str(data).encode("utf8")) + "\n")
    f.close()


with xlsxwriter.Workbook("DATA.xlsx") as workbook:
    worksheet = workbook.add_worksheet()
    for row_num, data in enumerate(zipped):
        worksheet.write_row(row_num, 0, data)

print("************DONE************")
