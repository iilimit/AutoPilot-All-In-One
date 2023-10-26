from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from colorama import Fore, Back, Style
import time
import csv
import pandas

options = Options()
service = Service(executable_path="B:\\Code Projects\\chromedriver.exe")
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://autopilot.dropshipcalendar.io/dashboard/import-list")

def scrapeItems():
    headers = ['Product Name', 'Quantity', 'Retail Price', 'Received', 'Profit', 'Amazon Link', 'Ebay Link']
    time.sleep(5)
    #search_product box
    driver.find_element(By.NAME, 'searchNewProduct').send_keys('1')
    #fufillment dropdown box
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[2]/form/div[1]/div/div[2]/div/div[1]/div').click()
    time.sleep(3)
    #fufilled button in dropdown box
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[2]/form/div[1]/div/div[2]/div/div[1]/div[2]/div[1]').click()

    userResponse = input("Type 'y' to start? ")
    if(userResponse == 'y'): 
        orderCard = driver.find_elements(By.CLASS_NAME, 'OrderItemCard_orderInfoBlock__3fqBw')
        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y %H,%M,%S")
        file_name = "products" + date_time + ".csv"

        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            for i in range(len(orderCard)):
                try:
                    incrementElementPosition = str(i+1)

                    profit = orderCard[i].find_element(By.CSS_SELECTOR, '#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' + incrementElementPosition + ') > div > div.OrderItemCard_rightPart__WV6mr > div.OrderItemCard_pictureAndInfoBlock__11j4O > div.OrderItemCard_infoBlock__OvHY- > div > div:nth-child(1) > p.OrderItemCard_partValue__pDDrD.OrderItemCard_green__f2YwU').text
                    profit = profit[1:]

                    quantity = orderCard[i].find_element(By.CSS_SELECTOR,'#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' + incrementElementPosition + ') > div > div.OrderItemCard_rightPart__WV6mr > div.OrderItemCard_pictureAndInfoBlock__11j4O > div.OrderItemCard_infoBlock__OvHY- > div > div:nth-child(4) > p.OrderItemCard_title__3Nkvz.OrderItemCard_dark__EFn8o').text
                    
                    if(float(profit)/int(quantity) < 0.8):
                        continue

                    title = orderCard[i].find_element(By.CSS_SELECTOR,'#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' + incrementElementPosition +') > div > div.OrderItemCard_leftPart__ykP4d > div.OrderItemCard_productTitlesBlock__KEfYT > a:nth-child(2) > p').text
                    title = title[2:]

                    received = orderCard[i].find_element(By.CSS_SELECTOR,'#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' + incrementElementPosition + ') > div > div.OrderItemCard_rightPart__WV6mr > div.OrderItemCard_pictureAndInfoBlock__11j4O > div.OrderItemCard_infoBlock__OvHY- > div > div:nth-child(2) > p.OrderItemCard_title__3Nkvz.OrderItemCard_dark__EFn8o').text
                    received = received[1:]

                    retail_price = orderCard[i].find_element(By.CSS_SELECTOR,'#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' + incrementElementPosition + ') > div > div.OrderItemCard_rightPart__WV6mr > div.OrderItemCard_pictureAndInfoBlock__11j4O > div.OrderItemCard_infoBlock__OvHY- > div > div:nth-child(3) > p').text
                    retail_price = retail_price[1:]

                    ebay_link = orderCard[i].find_element(By.CSS_SELECTOR,'#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' + incrementElementPosition + ') > div > div.OrderItemCard_leftPart__ykP4d > div.OrderItemCard_productTitlesBlock__KEfYT > a:nth-child(1)').get_attribute('href')

                    amazon_link = orderCard[i].find_element(By.CSS_SELECTOR,'#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form > div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk > div > div:nth-child(' + incrementElementPosition + ') > div > div.OrderItemCard_leftPart__ykP4d > div.OrderItemCard_productTitlesBlock__KEfYT > a:nth-child(2)').get_attribute('href')

                    data = [title, quantity, retail_price, received, profit, amazon_link, ebay_link]

                    writer.writerow(data)
                    print('Product #'+str(i)+ ' successfully scraped')
                except Exception as e:
                    print(e)
                    pass

def fillPrices():
    loop_amount = 0

    try:
        element = WebDriverWait(driver, timeout=500).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[3]/button[1]")))
        loop_amount = driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(9) > div > div > form > div.EditProduct_content__pL_TE > div > div.TabsNav_nav__2RQ7d.EditProduct_navTabs__xt7eH.TabsNav_dark__3zunU > div.TabsNav_itemsCount__1h5NM > p > span:nth-child(2)').text
    except Exception as e:
        print('Finding element took too much time')
    else: 
        for i in range(int(loop_amount)-1):
                time.sleep(2)
                #Gets ebay price from box
                ebay_price = driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(9) > div > div > form > div.EditProduct_content__pL_TE > div > div.rsw_2Y > div.rsw_2f.rsw_3G > div > div > div > div.ProductStoreParameters_prices__OkFiY > div.ProductStoreParameters_storesPricesBlock__28fx1 > a:nth-child(2) > p').text
                #formats price without $
                formatted_price = ebay_price.split('$')[1]
                #gets list price box element
                list_price_box = driver.find_element(By.XPATH, '//*[@id="basic-details.ebay.price"]')
                for i in range(6):
                    list_price_box.send_keys(Keys.BACK_SPACE)
                time.sleep(2)
                for i in range(len(formatted_price)):
                    time.sleep(0.5)
                    list_price_box.send_keys(formatted_price[i])
                
                time.sleep(1)
                #blank space
                driver.find_element(By.XPATH, '/html/body/div[2]/div/div/form/div[2]/div[2]').click()
                time.sleep(1)
                #next button
                driver.find_element(By.XPATH, '/html/body/div[2]/div/div/form/div[2]/div[3]/button[3]').click()

def fillPriceFromCSV():
    csvFile = pandas.read_csv('all_products.csv')

    loop_amount = 0

    try:
        element = WebDriverWait(driver, timeout=500).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[3]/button[1]")))
        loop_amount = driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(9) > div > div > form > div.EditProduct_content__pL_TE > div > div.TabsNav_nav__2RQ7d.EditProduct_navTabs__xt7eH.TabsNav_dark__3zunU > div.TabsNav_itemsCount__1h5NM > p > span:nth-child(2)').text
    except Exception as e:
        print('Finding element took too much time')
    else: 
        for i in range(int(loop_amount)-1):
            try:
                time.sleep(2)
                category = driver.find_element(By.CSS_SELECTOR, '#basic-details\.ebay\.category').get_attribute('value')
                if(category == ''):
                    time.sleep(1)
                    #next button
                    driver.find_element(By.XPATH, '/html/body/div[2]/div/div/form/div[2]/div[3]/button[3]').click()
                    continue
                product_name = driver.find_element(By.CSS_SELECTOR, '#basic-details\.ebay\.name').get_attribute('value')
                product_received_price = 0
                product_input_price = 0
                product = csvFile.loc[csvFile['Product Name'].str.contains(product_name, regex=False)]

                if not product.empty:
                    row_number = product.index
                    product_received_price = product.loc[row_number,'Received'].values[0]
                    product_quantity = product.loc[row_number,'Quantity'].values[0]
                    product_input_price = str(round(product_received_price/product_quantity, 2))
                    list_price_box = driver.find_element(By.XPATH, '//*[@id="basic-details.ebay.price"]')
                    for i in range(6):
                        list_price_box.send_keys(Keys.BACK_SPACE)
                    time.sleep(2)
                    for i in range(len(product_input_price)):
                        time.sleep(0.5)
                        list_price_box.send_keys(product_input_price[i])
                    
                    time.sleep(1)
                    #blank space
                    driver.find_element(By.XPATH, '/html/body/div[2]/div/div/form/div[2]/div[2]').click()
                    time.sleep(1)
                    #next button
                    driver.find_element(By.XPATH, '/html/body/div[2]/div/div/form/div[2]/div[3]/button[3]').click()
                    
            except Exception as e:
                print(e)
                pass

#User input to start module
userinput = ''
while(userinput!= '1' or userinput != '2' or userinput != '3'):
    print(Fore.GREEN + 'Welcome to a dropshipping All-In-One Tool!\n')
    print(Fore.YELLOW + '1. Item Scrapper\n2. Price Filler\n3. Price Filler From CSV\n')
    userinput = input(Fore.CYAN + "Select which module you want to use (type 'end' to stop): ")

    if(userinput == '1'):
        scrapeItems()
    elif(userinput == '2'):
        fillPrices()
    elif(userinput == '3'):
        fillPriceFromCSV()
    elif(userinput == 'end'):
        break
    else:
        print(Fore.RED + 'Invalid input. Please select another option.')
