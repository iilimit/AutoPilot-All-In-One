from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from colorama import Fore
import time
import csv
import pandas
import platform

platform = platform.system()
service = None
options = Options()
import_list_link = 'https://autopilot.dropshipcalendar.io/dashboard/import-list'
orders_link = 'https://autopilot.dropshipcalendar.io/dashboard/my-orders'
home_page_link = 'https://autopilot.dropshipcalendar.io/dashboard/home'

if(platform == 'Darwin'):
    service = Service(
    executable_path="macOS/chromedriver")
elif (platform == 'Windows'):
    service = Service(executable_path="windows/chromedriver.exe")

options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=service, options=options)
driver.get(import_list_link)



def scrapeItems():
    driver.get(orders_link)
    try:
        element = WebDriverWait(driver, timeout=500000).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_titleBlock__2tfXD.MyOrdersPage_titleBlock__2j-iX > div > button:nth-child(2)")))
    except Exception as e:
        print('Finding element took too much time')

    headers = ['Product Name', 'Quantity', 'Retail Price',
               'Received', 'Profit', 'Amazon Link', 'Ebay Link']
    time.sleep(5)
    # search_product box
    driver.find_element(By.NAME, 'searchNewProduct').send_keys('1')
    # fufillment dropdown box
    driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[2]/form/div[1]/div/div[2]/div/div[1]/div').click()
    time.sleep(3)
    # fufilled button in dropdown box
    driver.find_element(
        By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[2]/form/div[1]/div/div[2]/div/div[1]/div[2]/div[1]').click()
    userResponse = 'y'
    while(userResponse == 'y'):
        userResponse = input("Type 'y' to start? ")
        if(userResponse == 'y'):
            orderCard = driver.find_elements(
                By.CLASS_NAME, 'OrderItemCard_orderInfoBlock__3fqBw')
            now = datetime.now()
            date_time = now.strftime("%m-%d-%Y %H,%M,%S")
            file_name = "products" + date_time + ".csv"

            with open('all_products.csv', 'a', newline='') as file:
                writer = csv.writer(file)

                for i in range(len(orderCard)):
                    try:
                        incrementElementPosition = str(i+1)

                        profit = orderCard[i].find_element(By.CSS_SELECTOR, '#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' +
                                                        incrementElementPosition + ') > div > div.OrderItemCard_rightPart__WV6mr > div.OrderItemCard_pictureAndInfoBlock__11j4O > div.OrderItemCard_infoBlock__OvHY- > div > div:nth-child(1) > p.OrderItemCard_partValue__pDDrD.OrderItemCard_green__f2YwU').text
                        profit = profit[1:]

                        quantity = orderCard[i].find_element(By.CSS_SELECTOR, '#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' +
                                                            incrementElementPosition + ') > div > div.OrderItemCard_rightPart__WV6mr > div.OrderItemCard_pictureAndInfoBlock__11j4O > div.OrderItemCard_infoBlock__OvHY- > div > div:nth-child(4) > p.OrderItemCard_title__3Nkvz.OrderItemCard_dark__EFn8o').text

                        if(float(profit)/int(quantity) < 0.8):
                            raise Exception('Skipped item less than 0.8 profit')
                        
                        title = orderCard[i].find_element(By.CSS_SELECTOR, '#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' +
                                                        incrementElementPosition + ') > div > div.OrderItemCard_leftPart__ykP4d > div.OrderItemCard_productTitlesBlock__KEfYT > a:nth-child(2) > p').text
                        title = title[2:]

                        received = orderCard[i].find_element(By.CSS_SELECTOR, '#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' +
                                                            incrementElementPosition + ') > div > div.OrderItemCard_rightPart__WV6mr > div.OrderItemCard_pictureAndInfoBlock__11j4O > div.OrderItemCard_infoBlock__OvHY- > div > div:nth-child(2) > p.OrderItemCard_title__3Nkvz.OrderItemCard_dark__EFn8o').text
                        received = received[1:]

                        retail_price = orderCard[i].find_element(By.CSS_SELECTOR, '#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' +
                                                                incrementElementPosition + ') > div > div.OrderItemCard_rightPart__WV6mr > div.OrderItemCard_pictureAndInfoBlock__11j4O > div.OrderItemCard_infoBlock__OvHY- > div > div:nth-child(3) > p').text
                        retail_price = retail_price[1:]

                        ebay_link = orderCard[i].find_element(By.CSS_SELECTOR, '#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' +
                                                            incrementElementPosition + ') > div > div.OrderItemCard_leftPart__ykP4d > div.OrderItemCard_productTitlesBlock__KEfYT > a:nth-child(1)').get_attribute('href')

                        amazon_link = orderCard[i].find_element(By.CSS_SELECTOR, '#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' +
                                                                incrementElementPosition + ') > div > div.OrderItemCard_leftPart__ykP4d > div.OrderItemCard_productTitlesBlock__KEfYT > a:nth-child(2)').get_attribute('href')

                        data = [title, quantity, retail_price,
                                received, profit, amazon_link, ebay_link]

                        writer.writerow(data)
                        print('Product #' + str(i) + ' successfully scraped')
                    except Exception as e:
                        print('Item #' + str(i) + ' skipped due to error')
                        pass


def fillPrices():
    loop_amount = 0

    try:
        element = WebDriverWait(driver, timeout=500).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[3]/button[1]")))
        loop_amount = driver.find_element(
            By.CSS_SELECTOR, 'body > div:nth-child(9) > div > div > form > div.EditProduct_content__pL_TE > div > div.TabsNav_nav__2RQ7d.EditProduct_navTabs__xt7eH.TabsNav_dark__3zunU > div.TabsNav_itemsCount__1h5NM > p > span:nth-child(2)').text
    except Exception as e:
        print('Finding element took too much time')
    else:
        for i in range(int(loop_amount)-1):
            time.sleep(2)
            # Gets ebay price from box
            ebay_price = driver.find_element(
                By.CSS_SELECTOR, 'body > div:nth-child(9) > div > div > form > div.EditProduct_content__pL_TE > div > div.rsw_2Y > div.rsw_2f.rsw_3G > div > div > div > div.ProductStoreParameters_prices__OkFiY > div.ProductStoreParameters_storesPricesBlock__28fx1 > a:nth-child(2) > p').text
            # formats price without $
            formatted_price = ebay_price.split('$')[1]
            # gets list price box element
            list_price_box = driver.find_element(
                By.XPATH, '//*[@id="basic-details.ebay.price"]')
            for i in range(6):
                list_price_box.send_keys(Keys.BACK_SPACE)
            time.sleep(1)
            for i in range(len(formatted_price)):
                time.sleep(0.1)
                list_price_box.send_keys(formatted_price[i])

            time.sleep(1)
            # blank space
            driver.find_element(
                By.XPATH, '/html/body/div[2]/div/div/form/div[2]/div[2]').click()
            time.sleep(1)
            # next button
            driver.find_element(
                By.XPATH, '/html/body/div[2]/div/div/form/div[2]/div[3]/button[3]').click()


def fillPriceFromCSV():
    #change path to relative
    csvFile = pandas.read_csv('all_products.csv')

    loop_amount = 0

    try:
        element = WebDriverWait(driver, timeout=500).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[3]/button[1]")))
        loop_amount = driver.find_element(
            By.CSS_SELECTOR, 'body > div:nth-child(9) > div > div > form > div.EditProduct_content__pL_TE > div > div.TabsNav_nav__2RQ7d.EditProduct_navTabs__xt7eH.TabsNav_dark__3zunU > div.TabsNav_itemsCount__1h5NM > p > span:nth-child(2)').text
    except Exception as e:
        print('Finding element took too much time')
    else:
        for i in range(int(loop_amount)-1):
            try:
                time.sleep(2)
                category = driver.find_element(
                    By.CSS_SELECTOR, '#basic-details\.ebay\.category').get_attribute('value')
                if(category == ''):
                    # time.sleep(1)
                    # next button
                    driver.find_element(By.XPATH, '/html/body/div[2]/div/div/form/div[2]/div[3]/button[3]').click()
                    continue

                product_name = driver.find_element(
                    By.CSS_SELECTOR, '#basic-details\.ebay\.name').get_attribute('value')
                product_received_price = 0
                product_input_price = 0
                product = csvFile.loc[csvFile['Product Name'].str.contains(
                    product_name, regex=False)]

                if not product.empty:
                    row_number = product.index
                    product_received_price = product.loc[row_number,
                                                         'Received'].values[0]
                    product_quantity = product.loc[row_number,
                                                   'Quantity'].values[0]
                    product_input_price = str(
                        round(product_received_price/product_quantity, 2))
                    list_price_box = driver.find_element(
                        By.XPATH, '//*[@id="basic-details.ebay.price"]')
                    for i in range(6):
                        list_price_box.send_keys(Keys.BACK_SPACE)
                    time.sleep(1)
                    for i in range(len(product_input_price)):
                        time.sleep(0.1)
                        list_price_box.send_keys(product_input_price[i])

                    time.sleep(1)
                    # blank space
                    driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/form/div[2]/div[2]').click()
                    time.sleep(1)
                    # next button
                    driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/form/div[2]/div[3]/button[3]').click()
                else: 
                    driver.find_element(
                        By.XPATH, '/html/body/div[2]/div/div/form/div[2]/div[3]/button[3]').click()
                    continue
            except Exception as e:
                print(e)
                pass

def removeBadProducts():
    items_clicked = 0
    time.sleep(2)

    item_cards = driver.find_elements(By.CLASS_NAME, 'ImportListItem_itemContainer__Wsg7n')

    #this is for full item cards: ImportListItem_item__14UhT ImportListPage_importListItem__3pCc8 ImportListItem_dark__3-oKJ
    item_cards = driver.find_elements(By.CLASS_NAME, 'ImportListItem_itemContainer__Wsg7n')
    for i in range(len(item_cards)):
        index = i+1
        try:
            price = item_cards[i].find_element(By.CLASS_NAME, 'Input_input__2YO5c Input_dark__2BS-o InputWithIcon_input__19Tyt ImportListItem_input__2qyns InputWithIcon_dark__2F_nG').text
            # price2 = item_cards[i].find_element(By.XPATH, '//*[@id="products[0].profits[0]"]').text
            hasVeroMessage = item_cards[i].find_element(By.CLASS_NAME,'ImportListItem_veroMessage__cdkzG').size()
            
            # print(price[:1])
            if(hasVeroMessage > 0 or price[:1] == '-'):
                driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[3]/div/div[{index}]/div/div[1]/label').click()
                items_clicked += 1
        except NoSuchElementException:
            print('Element is not found')
        except Exception as e:
                pass
            
    #deletes selected items
    if(items_clicked > 0):
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[1]/div/div[1]/div/div/div[1]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[1]/div/div[1]/div/div/div[2]/div[2]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/button[2]').click()
        
        
#User input to start module
userinput = ''
while(userinput != '1' or userinput != '2' or userinput != '3'):
    print(Fore.GREEN + 'Welcome to a dropshipping All-In-One Tool!\n')
    print(Fore.YELLOW + '1. Item Scrapper\n2. Price Filler\n3. Price Filler From CSV\n4. Remove Bad Products')
    userinput = input(Fore.CYAN + "Select which module you want to use (type 'end' to stop): ")

    if(userinput == '1'):
        continue
    elif(userinput == '2'):
        continue
    elif(userinput == '3'):
        continue
    elif(userinput == '4'):
        removeBadProducts()
    elif(userinput == 'end'):
        break
    else:
        print(Fore.RED + 'Invalid input. Please select another option.')
