from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import urllib.request
import datetime
import pymongo

options = webdriver.ChromeOptions()
options.add_argument('--headless')

#Download chrome selenium webdriver and provide path to executable
driver = webdriver.Chrome(r'C:\Users\IBK\Downloads\chromedriver_win32\chromedriver.exe', options=options)

products = []
variants = []
prices = []
# images = []
desc = []
count = 0
get_count = 0

#Link to start grabbing items from.
driver.get('https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&marketplace=FLIPKART&p%5B%5D=facets.type%255B%255D%3DSmartphones')
driver.implicitly_wait(10)

while True:
    time.sleep(1)
    #Workaround for lazy loaded images
    elements = driver.find_elements_by_class_name('_2kHMtA')
    for data in elements:
        coor = data.location_once_scrolled_into_view
        driver.execute_script('window.scrollTo({}, {});'.format(coor['x'], coor['y']))
    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    #Common classname that holds the data
    for a in soup.find_all('div', attrs={'class': '_2kHMtA'}):
        driver.implicitly_wait(10)
        name = a.find('div', attrs={'class': '_4rR01T'})
        price = a.find('div', attrs={'class': '_3I9_wc _27UcVY'})
        sale = a.find('div', attrs={'class': '_30jeq3 _1_WHN1'})
#         image = a.find('div', attrs={'class': '_3BTv9X'}).find('img').get('src')
        des = a.find('ul', attrs={'class': '_1xgFaf'})
        try:
            products.append(name.text)
            variants.append(name.text.split(', ')[1].split(')')[0])
        except:
            products.append("")
        try:
            test = ''.join(i for i in price.text if i.isdigit())
            prices.append(test)
        except:
            test = ''.join(i for i in sale.text if i.isdigit())
            prices.append(test)
#         try:
#             split_data = name.text.split(' (')
#             slug = split_data[0] + '_' + split_data[1].split(',')[0]
#             urllib.request.urlretrieve(image, f"images\{slug}.jpg")
#             images.append(slug)
#         except:
#             #If retrieved item was not lazy loaded, delete current entry and continue
#             del prices[-1]
#             del products[-1]
#             del variants[-1]
#             continue
        try:
            desc.append(des.get_text('\n', strip=True))
        except:
            desc.append("")
    print(len(products))
    #Scrolling to top of page
    driver.execute_script("window.scrollTo(0, 0);")

    #Finding the next page button
    nxt_btn = driver.find_elements_by_class_name('_1LKTO3')
    if len(products) > 5:
        break
    if count == 0:
        count += 1
        nxt_btn[0].click()
        continue
    elif len(nxt_btn) > 1:
        count += 1
        nxt_btn[1].click()
        continue
    else:
        break
print("products length " , len(products))
print(products)
print("prices length " , len(prices))
print("sales length " , len(sale))
print("desc length " , len(desc))

# df = pd.DataFrame({'Product Name': products, 'Variants': variants, 'Price': prices, 'Description': desc})
# df.to_csv('new.csv', index=False, encoding='utf-8')


def Convert(lst , v , p , d):
    res = []
    for i in range(len(lst)):
        a = {'name': lst[i] , 'variants' : v[i] , 'price' : p[i] , 'description' : d[i]}
        dc = a.copy()
        res.append(dc)
        
    return res
         
# Driver code
print(Convert(products , variants , prices , desc))
result = Convert(products , variants , prices , desc)


client = pymongo.MongoClient("mongodb+srv://ibk2510:deathbychocolate@cluster0.u4lph.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.test
# test
db = client['Electronics']
# define collection
collection = db['smartphones']
# sample data
x = collection.insert_many(result)
print(x)