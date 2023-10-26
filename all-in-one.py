from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from colorama import Fore, Back, Style
import time
import csv

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

userinput = ''
while(userinput!= '1' or userinput != '2' or userinput != '3'):
    print(Fore.GREEN + 'Welcome to a dropshipping All-In-One Tool!\n')
    print(Fore.YELLOW + '1. Item Scrapper\n2. Price Filler\n3. Price Filler From CSV\n')
    userinput = input(Fore.CYAN + 'Select which module you want to use: ')

    if(userinput == '1'):
        scrapeItems()
    elif(userinput == '2'):
        fillPrices()
    elif(userinput == '3'):
        fillPriceFromCSV()
    else:
        print(Fore.RED + 'Invalid input. Please select another option.')
