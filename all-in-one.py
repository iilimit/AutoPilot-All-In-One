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
driver.get("https://autopilot.dropshipcalendar.io/dashboard/home")
import_list_link = 'https://autopilot.dropshipcalendar.io/dashboard/import-list'
orders_link = 'https://autopilot.dropshipcalendar.io/dashboard/my-orders'

def removeBadProducts():
    items_clicked = 0
    driver.get(import_list_link)
    time.sleep(7)

    #this is for full item cards: ImportListItem_item__14UhT ImportListPage_importListItem__3pCc8 ImportListItem_dark__3-oKJ
    item_cards = driver.find_elements(By.CLASS_NAME, 'ImportListItem_itemContainer__Wsg7n')

    for i in range(len(item_cards)):
        index = i+1
        try:
            price = item_cards[i].find_element(By.XPATH,f'//*[@id="products[{i}].profits[0]"]').get_attribute("value")
            # price2 = item_cards[i].find_element(By.XPATH, '//*[@id="products[0].profits[0]"]').text
            # hasVeroMessage = item_cards[i].find_element(By.CLASS_NAME,'ImportListItem_veroMessage__cdkzG').size()
            
            if(price[:1] == '-'):
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
