import requests, time, chromedriver_autoinstaller, xlsxwriter
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
#Name Camping Platz
camp_name = []
#Ort
camp_location = []
#Bewertung
camp_rating = []
#Bewertungen
camp_ratings = []
#Preis Hauptsaison
camp_saisonM = []
#Preis Nebensaison
camp_saisonS = []
#Max Anzahl Stellplätze
camp_park = []
#Anzahl Touristen Stellplätze
camp_parkT = []
#Adress
camp_adress = []
#Tel
camp_phone = []
#Fax
camp_fax = []
#Website
camp_website = []
#Öffnungszeiten
camp_open = []

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()
driver.get("https://www.camping.info/de/suche?q=Deutschland")
driver.maximize_window()
time.sleep(2)

loop = True
while loop == True:
    try:
        action = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/div/div/div[3]/div/div/div/button[3]')
        action.click()
        loop = False
    except NoSuchElementException:
        print("[!] Cant accept cookies yet!")
        time.sleep(2)
print("[*] Accepted cookies.")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
print("[*] Scrolled down.")
time.sleep(2)
action = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div[3]/div[2]/section[3]/div/ul/li[8]')
action.click()
print("[*] Found button and moved to last page.")
time.sleep(2)
element = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/main/div/div[3]/div[2]/section[3]/div/ul/li[6]')
maxpage = int(str(element.text).strip(" "))
nowpage = -1
print("[*] Search has "+str(maxpage)+" pages.")

mainloop = True
while mainloop == True:
    nowpage += 1
    if nowpage == (maxpage):
        mainloop = False
    print("Page "+str(nowpage + 1)+"/"+str(maxpage))
    if   nowpage * 15 == 0:
        driver.get("https://www.camping.info/de/suche?q=Deutschland")
    else:
        end = nowpage * 15
        url = "https://www.camping.info/de/land/deutschland?offset="+str(end)
        driver.get(url)
    time.sleep(2)
    html  = driver.page_source
    soup  = BeautifulSoup(html, "html.parser")
    items = soup.find_all('li', class_="result-list__item")
    y     = 0
    for item in items:
        y += 1
    x     = 0
    for item in items:
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        x += 1
        area = ""
        print("Item "+str(x)+"/"+str(y))
        print("\n")
        try:
            print("NAME             :"+str(item.find('h2', class_="text-black headline-name tile__headline text-ellipsis headline-name--premium").text)) 
            camp_name.append(str(item.find('h2', class_="text-black headline-name tile__headline text-ellipsis headline-name--premium").text))
        except AttributeError:
            try:
                print("NAME             :"+str(item.find('h2', class_="text-black headline-name tile__headline text-ellipsis").text)) 
                camp_name.append(str(item.find('h2', class_="text-black headline-name tile__headline text-ellipsis").text))
            except AttributeError:
                print("NO NAME FOUND    : NO NAME FOUND")
                camp_name.append("NONE FOUND")
        try:
            print("AREA                 :"+str(item.find('h3', class_="tile__subline text-normal text-gray text-ellipsis mb-0").text)) 
            area = str(item.find('h3', class_="tile__subline text-normal text-gray text-ellipsis mb-0").text)
        except AttributeError:
            print("NO AREA FOUND        : NO RATINGS FOUND")
            area = "???"
        try:
            print("RATING               : "+str(item.find('small', class_="rating-text text-black text-bold text-uppercase").text)+" ("+str(item.find('span', class_="circular-text text-black rating-radial__value mb-0 campsite__rating-font strong").text)+")")
            camp_rating.append(str(item.find('small', class_="rating-text text-black text-bold text-uppercase").text)+" ("+str(item.find('span', class_="circular-text text-black rating-radial__value mb-0 campsite__rating-font strong").text)+")")
            print("RATINGS              : "+str(item.find('small', class_="rating-count text-black").text))
            camp_ratings.append(str(item.find('small', class_="rating-count text-black").text))
        except AttributeError:
            print("NO RATINGS FOUND     : NO RATINGS FOUND")
            camp_rating.append("NONE FOUND")
            camp_ratings.append("NONE FOUND")
        detail_page = '//*[@id="app"]/div/div/main/div/div[3]/div[2]/section[2]/ul/li['+str(x)+']/a/div/div[3]/div[3]/div[2]/span'
        actionloop = True
        while actionloop == True:
            try:
                action = driver.find_element(By.XPATH, detail_page)#get last details
                action.click()
                actionloop = False
            except NoSuchElementException:
                try:
                    time.sleep(2)
                    action = driver.find_element(By.XPATH, detail_page)#get last details
                    action.click()
                    actionloop = False
                except NoSuchElementException:
                    pass
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        try:
            element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div[2]/div[2]/div[2]/div[1]/div/ul/li[1]/span')
            element2= driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div[2]/div[2]/div[2]/div[1]/div/ul/li[2]/span')
            print("COUNTRY              : "+str(element.get_attribute("textContent"))+" / "+str(element2.get_attribute("textContent")))
            area = str(element.get_attribute("textContent"))+" / "+str(element2.get_attribute("textContent")) + " / " + area
        except NoSuchElementException:
            print("NO COUNTRY FOUND     : NO COUNTRY FOUND")
            area = "???"+area
            camp_location.append(area)
        try:
            element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div[2]/div[2]/div[3]/div[1]/div[1]/small[1]')
            print("MAIN SAISON          : "+str(element.get_attribute("textContent")))
            camp_saisonM.append(str(element.get_attribute("textContent")))
            element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div[2]/div[2]/div[3]/div[1]/div[1]/small[2]')
            print("SIDE SAISON          : "+str(element.get_attribute("textContent")))
            camp_saisonS.append(str(element.get_attribute("textContent")))
        except NoSuchElementException:
            print("NO MAIN SAISON FOUND : NO MAIN SAISON FOUND")
            camp_saisonM.append("NONE FOUND")
            print("NO SIDE SAISON FOUND : NO SIDE SAISON FOUND")
            camp_saisonS.append("NONE FOUND")
        try:
            element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/section[4]/div[2]/div[2]/div[3]/div/div[2]/a')
            print("LINK TO WEBSITE      : "+str(element.get_attribute("textContent")))
            camp_website.append(str(element.get_attribute("textContent")))
        except NoSuchElementException:
            print("NO WEBSITE FOUND     : NO WEBSITE FOUND")
            camp_website.append("NONE FOUND")
        try:
            element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/section[3]/div[2]/div/div[4]/div/div[2]/div[1]/div/span[2]')
            print("MAX STELLPLATZE      : "+str(element.get_attribute("textContent")))
            camp_park.append(str(element.get_attribute("textContent")))
        except NoSuchElementException:
            print("NO STPLTZ FOUND      : NO STPLTZ FOUND")
            camp_park.append("NONE FOUND")
        try:
            element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/section[3]/div[2]/div/div[4]/div/div[2]/div[2]/div/span[2]')
            print("MAX STELLPLATZE T    : "+str(element.get_attribute("textContent")))
            camp_parkT.append(str(element.get_attribute("textContent")))
        except NoSuchElementException:
            print("NO STPLTZ T FOUND    : NO STPLTZ T FOUND")
            camp_parkT.append("NONE FOUND")
        try:
            element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/section[4]/div[2]/div[2]/div[1]/div/div[2]/a')
            print("ADRESS               : "+str(element.get_attribute("textContent")))
            camp_adress.append(str(element.get_attribute("textContent")))
        except NoSuchElementException:
            try:
                element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/section[5]/div[2]/div[2]/div[1]/div/div[2]/a')
                print("ADRESS (2)           : "+str(element.get_attribute("textContent")))
                camp_adress.append(str(element.get_attribute("textContent")))
            except NoSuchElementException:
                print("NO ADRESS FOUND      : NO ADRESS FOUND")
                camp_adress.append("NONE FOUND")
        try:
            element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/section[4]/div[2]/div[2]/div[2]/div/div[2]/a')
            print("PHONE                : "+str(element.get_attribute("textContent")))
            camp_phone.append(str(element.get_attribute("textContent")))
        except NoSuchElementException:
            try:
                element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/section[5]/div[2]/div[2]/div[2]/div/div[2]/a')
                print("PHONE (2)            : "+str(element.get_attribute("textContent")))
                camp_phone.append(str(element.get_attribute("textContent")))
            except NoSuchElementException:
                print("NO PHONE FOUND   : NO PHONE FOUND")
                camp_phone.append("NONE FOUND")
        try:
            element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/section[4]/div[2]/div[2]/div[2]/div/div[4]')
            print("FAX                  : "+str(element.get_attribute("textContent")))
            camp_fax.append(str(element.get_attribute("textContent")))
        except NoSuchElementException:
            try:
                element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/section[5]/div[2]/div[2]/div[2]/div/div[4]')
                print("FAX (2)              : "+str(element.get_attribute("textContent")))
                camp_fax.append(str(element.get_attribute("textContent")))
            except NoSuchElementException:
                print("NO FAX FOUND         : NO FAX FOUND")
                camp_fax.append("NONE FOUND")
        try:
            element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/section[4]/div[2]/div[2]/div[4]/div/div[2]/span')
            print("OPENING TIMES        : "+str(element.get_attribute("textContent")))
            camp_open.append(str(element.get_attribute("textContent")))
        except NoSuchElementException:
            try:
                element = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/section[5]/div[2]/div[2]/div[4]/div/div[2]/span')
                print("OPENING TIMES (2)    : "+str(element.get_attribute("textContent")))
                camp_open.append(str(element.get_attribute("textContent")))
            except NoSuchElementException:
                print("NO OPEN TIMES FOUND  : NO OPEN TIMES FOUND")
                camp_open.append("NONE FOUND")
        print("_____________________________________________________________")
        driver.execute_script("window.history.go(-1)")
driver.quit()

camp_name.insert(    0,"CAMP NAMES")
camp_location.insert(0,"CAMP LOCATION")
camp_rating.insert(  0,"CAMP RATING")
camp_ratings.insert( 0,"CAMP RATINGS")
camp_saisonM.insert( 0,"CAMP MAIN SAISON")
camp_saisonS.insert( 0,"CAMP SIDE SAISON")
camp_park.insert(    0,"CAMP STELLPLATZE")
camp_parkT.insert(   0,"CAMP STELLPLATZE TOURISTEN")
camp_adress.insert(  0,"CAMP ADRESS")
camp_phone.insert(   0,"CAMP PHONE")
camp_fax.insert(     0,"CAMP FAX")
camp_website.insert( 0,"CAMP WEBSITE")
camp_open.insert(    0,"CAMP OPEN TIMES")
zipped = zip(camp_name,camp_location,camp_rating,camp_ratings,camp_saisonM,camp_saisonS,camp_park,camp_parkT,camp_adress,camp_phone,camp_fax,camp_website,camp_open)

with open('camp_name.txt', 'w+') as f:
    for line in camp_name:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_location.txt', 'w+') as f:
    for line in camp_location:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_rating.txt', 'w+') as f:
    for line in camp_rating:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_ratings.txt', 'w+') as f:
    for line in camp_ratings:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_saisonM.txt', 'w+') as f:
    for line in camp_saisonM:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_saisonS.txt', 'w+') as f:
    for line in camp_saisonS:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_park.txt', 'w+') as f:
    for line in camp_park:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_parkT.txt', 'w+') as f:
    for line in camp_parkT:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_adress.txt', 'w+') as f:
    for line in camp_adress:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_phone.txt', 'w+') as f:
    for line in camp_phone:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_fax.txt', 'w+') as f:
    for line in camp_fax:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_website.txt', 'w+') as f:
    for line in camp_website:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open('camp_open.txt', 'w+') as f:
    for line in camp_open:
        f.write(str(str(line).encode("utf8")) + "\n")
    f.close()

with open("DATA.txt","w+") as f:
    for data in zipped:
        f.write(str(str(data).encode("utf8")) + "\n")
    f.close()

with open("DATA2.txt","w+") as f:
    for data in zipped:
        f.write(str(str(data).encode("utf8")) + "\n")

with xlsxwriter.Workbook("CAMPDATA.xlsx") as workbook:
    worksheet = workbook.add_worksheet()
    for row_num, data in enumerate(zipped):
        worksheet.write_row(row_num, 0, data)

print("************DONE************")
