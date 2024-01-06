from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from colorama import Fore
import time
import csv
import pandas
import platform
from bs4 import BeautifulSoup
import requests

result = requests.get('https://www.ebay.com/sch/26395/i.html?_from=R40&_nkw=DEODORANT+')
doc = BeautifulSoup(result.text, "html.parser")
links = []

for link in doc.find_all("a", class_="s-item__link"):
    links.append(link.get('href'))
    

# platform = platform.system()
# service = None
# options = Options()
# import_list_link = 'https://autopilot.dropshipcalendar.io/dashboard/import-list'
# orders_link = 'https://autopilot.dropshipcalendar.io/dashboard/my-orders'
# home_page_link = 'https://autopilot.dropshipcalendar.io/dashboard/home'

# if(platform == 'Darwin'):
#     service = Service(executable_path="macOS/chromedriver")
# elif (platform == 'Windows'):
#     service = Service(executable_path="windows/chromedriver.exe")
    
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
# driver = webdriver.Chrome(service=service, options=options)
# driver.get(import_list_link)


# def scrapeEbayStores():

        
#User input to start module
# userinput = ''
# while(userinput != '1' or userinput != '2' or userinput != '3'):
#     print(Fore.GREEN + 'Welcome to a dropshipping All-In-One Tool!\n')
#     print(Fore.YELLOW + '1. Item Scrapper\n2. Price Filler\n3. Price Filler From CSV\n4. Remove Bad Products')
#     userinput = input(Fore.CYAN + "Select which module you want to use (type 'end' to stop): ")

#     if(userinput == '1'):
#         scrapeItems()
#     elif(userinput == '2'):
#         fillPrices()
#     elif(userinput == '3'):
#         fillPriceFromCSV()
#     elif(userinput == '4'):
#         removeBadProducts()
#     elif(userinput == '5'):
#         scrapeEbayStores()
#     elif(userinput == 'end'):
#         break
#     else:
#         print(Fore.RED + 'Invalid input. Please select another option.')
