"""
All in one tool for dropshipping
Ability to scrape items, auto fill prices, remove bad products, etc.
"""
import platform
import time
import csv
import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from colorama import Fore, init

platform = platform.system()
SERVICE = None
options = Options()
IMPORT_LIST_LINK = "https://autopilot.dropshipcalendar.io/dashboard/import-list"
ORDERS_LINK = "https://autopilot.dropshipcalendar.io/dashboard/my-orders"
HOME_PAGE_LINK = "https://autopilot.dropshipcalendar.io/dashboard/home"
ERROR_NO_ELEMENT = "Finding element took too much time"

if platform == "Darwin":
    service = Service(executable_path="macOS/chromedriver")
elif platform == "Windows":
    service = Service(executable_path="windows/chromedriver.exe")

options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(service=service, options=options)
init()
driver.get("https://autopilot.dropshipcalendar.io/dashboard/home")
IMPORT_LIST_LINK = "https://autopilot.dropshipcalendar.io/dashboard/import-list"
ORDERS_LINK = "https://autopilot.dropshipcalendar.io/dashboard/my-orders"

driver.get(IMPORT_LIST_LINK)


# define Python user-defined exceptions
class ProfitBelowThreshold(Exception):
    "Raised when scraped profit is below specified value"


def select_shown_items_filter(filter_amount: int):
    """
    Selects an option from the filter to show a certain amount of items on the page.

    Keyword arguments:
    filter_amount -- Amount of items that will be shown (Must be 10, 20, 50, 100, or 200)
    """
    valid_filters = [10, 20, 50, 100, 200]
    if filter_amount not in valid_filters:
        raise ValueError(
            f"{filter_amount} is not a valid filter amount. It must be {valid_filters}."
        )

    try:
        filter_dropdown = WebDriverWait(driver, timeout=500000).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[4]/div/div/div',
                )
            )
        )
    except NoSuchElementException:
        print(ERROR_NO_ELEMENT)
    # filter_dropdown = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[4]/div/div/div')
    filter_dropdown.click()

    filters = driver.find_elements(
        By.CSS_SELECTOR,
        "#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.ImportListPage_page__2TVxh.dark > div > div.Page_content__1d0Vb.ImportListPage_content__1ZKal > form > div.Pagination_paginationWrapper__yuZIA.ImportListPage_paginationBlock__2hUls.Pagination_withSelectCount__wcCl5.Pagination_dark__3k7yM > div > div > div.Dropdown_list__3Zdmf.Dropdown_top__3f1Fd.Dropdown_right__2MCMx.Pagination_dropdownList__PauGX.Dropdown_dark__2UE8M > div",
    )

    if filter_amount == valid_filters[0]:
        filters[0].click()
    elif filter_amount == valid_filters[1]:
        filters[1].click()
    elif filter_amount == valid_filters[2]:
        filters[2].click()
    elif filter_amount == valid_filters[3]:
        filters[3].click()
    elif filter_amount == valid_filters[4]:
        filters[4].click()


def has_prev_page() -> bool:
    """
    Checks if the previous page button is active
    """
    try:
        is_prev_page_button_disabled = driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[4]/ul/li[1]/a',
        ).get_attribute("aria-disabled")
        if is_prev_page_button_disabled == "true":
            return False
        return True
    except NoSuchElementException:
        return True


def click_prev_page_button():
    """
    Clicks the previous page button if it is active
    """
    prev_page_button = driver.find_element(
        By.XPATH,
        '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[4]/ul/li[1]',
    )
    if has_prev_page():
        prev_page_button.click()


def scrape_items():
    """
    Scrapes items from the amount of pages the user inputs

    Returns:
        A CSV file with all scraped items:
        Product Name, Quantity, Retail Price, Received, Profit, Amazon Link, and Ebay Link
    """
    scraped_item_counter = 0
    amount_of_items = 0
    driver.get(ORDERS_LINK)
    try:
        WebDriverWait(driver, timeout=500000).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    (
                        "#root > div > div.Dashboard_fullPage__1_NVb >"
                        " div.Dashboard_main__3DhrS >"
                        " div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div >"
                        " div.Page_titleBlock__2tfXD.MyOrdersPage_titleBlock__2j-iX >"
                        " div > button:nth-child(2)"
                    ),
                )
            )
        )
    except NoSuchElementException:
        print(ERROR_NO_ELEMENT)

    time.sleep(5)
    # search_product box
    driver.find_element(By.NAME, "searchNewProduct").send_keys("1")
    # fufillment dropdown box
    driver.find_element(
        By.XPATH,
        '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[2]/form/div[1]/div/div[2]/div/div[1]/div',
    ).click()
    time.sleep(3)
    # fufilled button in dropdown box
    driver.find_element(
        By.XPATH,
        (
            '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[2]/form/div[1]/div/div[2]/div/div[1]/'
            "div[2]/div[1]"
        ),
    ).click()

    amount_of_pages = input("How many pages do you want to scrape? ")
    floor_profit_amount = 1

    for j in range(int(amount_of_pages)):
        try:
            WebDriverWait(driver, timeout=500000).until(
                EC.visibility_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        (
                            "#root > div > div.Dashboard_fullPage__1_NVb >"
                            " div.Dashboard_main__3DhrS >"
                            " div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div"
                            " > div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 >"
                            " form >"
                            " div.ProductsFormContent_productsWrapper__38CQo"
                            ".MyOrdersPage_itemsListWrapper__1kbCk"
                            " > div > div:nth-child(1) > div >"
                            " div.OrderItemCard_rightPart__WV6mr >"
                            " div.OrderItemCard_pictureAndInfoBlock__11j4O >"
                            " div.OrderItemCard_infoBlock__OvHY- > p"
                        ),
                    )
                )
            )
        except NoSuchElementException:
            print(ERROR_NO_ELEMENT)

        order_card = driver.find_elements(
            By.CLASS_NAME, "OrderItemCard_orderInfoBlock__3fqBw"
        )

        with open("all_products.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # scrapes item's title, profit, quantity, retail price, ebay link, and amazon link then appends to the csv
            for i, card in enumerate(order_card):
                try:
                    increment_element_position = str(i + 1)

                    profit = card.find_element(
                        By.CSS_SELECTOR,
                        "#root > div > div.Dashboard_fullPage__1_NVb >"
                        " div.Dashboard_main__3DhrS >"
                        " div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div >"
                        " div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form >"
                        " div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk"
                        " > div > div:nth-child("
                        + increment_element_position
                        + ") > div > div.OrderItemCard_rightPart__WV6mr >"
                        " div.OrderItemCard_pictureAndInfoBlock__11j4O >"
                        " div.OrderItemCard_infoBlock__OvHY- > div >"
                        " div:nth-child(1) >"
                        " p.OrderItemCard_partValue__pDDrD.OrderItemCard_green__f2YwU",
                    ).text
                    profit = profit[1:]

                    quantity = card.find_element(
                        By.CSS_SELECTOR,
                        "#root > div > div.Dashboard_fullPage__1_NVb >"
                        " div.Dashboard_main__3DhrS >"
                        " div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div >"
                        " div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form >"
                        " div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk"
                        " > div > div:nth-child("
                        + increment_element_position
                        + ") > div > div.OrderItemCard_rightPart__WV6mr >"
                        " div.OrderItemCard_pictureAndInfoBlock__11j4O >"
                        " div.OrderItemCard_infoBlock__OvHY- > div >"
                        " div:nth-child(4) >"
                        " p.OrderItemCard_title__3Nkvz.OrderItemCard_dark__EFn8o",
                    ).text

                    profit_after_quantity = float(profit) / int(quantity)
                    if profit_after_quantity < floor_profit_amount:
                        raise ProfitBelowThreshold

                    title = card.find_element(
                        By.CSS_SELECTOR,
                        "#root > div > div.Dashboard_fullPage__1_NVb >"
                        " div.Dashboard_main__3DhrS >"
                        " div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div >"
                        " div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form >"
                        " div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk"
                        " > div > div:nth-child("
                        + increment_element_position
                        + ") > div > div.OrderItemCard_leftPart__ykP4d >"
                        " div.OrderItemCard_productTitlesBlock__KEfYT >"
                        " a:nth-child(2) > p",
                    ).text
                    title = title[2:]

                    received = card.find_element(
                        By.CSS_SELECTOR,
                        "#root > div > div.Dashboard_fullPage__1_NVb >"
                        " div.Dashboard_main__3DhrS >"
                        " div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div >"
                        " div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form >"
                        " div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk"
                        " > div > div:nth-child("
                        + increment_element_position
                        + ") > div > div.OrderItemCard_rightPart__WV6mr >"
                        " div.OrderItemCard_pictureAndInfoBlock__11j4O >"
                        " div.OrderItemCard_infoBlock__OvHY- > div >"
                        " div:nth-child(2) >"
                        " p.OrderItemCard_title__3Nkvz.OrderItemCard_dark__EFn8o",
                    ).text
                    received = received[1:]

                    retail_price = card.find_element(
                        By.CSS_SELECTOR,
                        "#root > div > div.Dashboard_fullPage__1_NVb >"
                        " div.Dashboard_main__3DhrS >"
                        " div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div >"
                        " div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form >"
                        " div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk"
                        " > div > div:nth-child("
                        + increment_element_position
                        + ") > div > div.OrderItemCard_rightPart__WV6mr >"
                        " div.OrderItemCard_pictureAndInfoBlock__11j4O >"
                        " div.OrderItemCard_infoBlock__OvHY- > div >"
                        " div:nth-child(3) > p",
                    ).text
                    retail_price = retail_price[1:]

                    ebay_link = card.find_element(
                        By.CSS_SELECTOR,
                        "#root > div > div.Dashboard_fullPage__1_NVb >"
                        " div.Dashboard_main__3DhrS >"
                        " div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div >"
                        " div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form >"
                        " div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk"
                        " > div > div:nth-child("
                        + increment_element_position
                        + ") > div > div.OrderItemCard_leftPart__ykP4d >"
                        " div.OrderItemCard_productTitlesBlock__KEfYT >"
                        " a:nth-child(1)",
                    ).get_attribute("href")

                    amazon_link = card.find_element(
                        By.CSS_SELECTOR,
                        "#root > div > div.Dashboard_fullPage__1_NVb >"
                        " div.Dashboard_main__3DhrS >"
                        " div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div >"
                        " div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form >"
                        " div.ProductsFormContent_productsWrapper__38CQo.MyOrdersPage_itemsListWrapper__1kbCk"
                        " > div > div:nth-child("
                        + increment_element_position
                        + ") > div > div.OrderItemCard_leftPart__ykP4d >"
                        " div.OrderItemCard_productTitlesBlock__KEfYT >"
                        " a:nth-child(2)",
                    ).get_attribute("href")

                    data = [
                        title,
                        quantity,
                        retail_price,
                        received,
                        profit,
                        amazon_link,
                        ebay_link,
                    ]

                    writer.writerow(data)
                    scraped_item_counter += 1
                    amount_of_items += 1
                    print(Fore.GREEN + f"Product #{str(i)} successfully scraped")
                except ProfitBelowThreshold:
                    print(
                        Fore.RED
                        + f"Skipped due to profit <{profit_after_quantity}> below"
                        f" <{floor_profit_amount}>"
                    )
                    amount_of_items += 1
                except NoSuchElementException:
                    print(Fore.RED + "Skipped due to element not found")
                    amount_of_items += 1
                    continue
        # click next page button
        driver.find_element(
            By.CSS_SELECTOR,
            (
                "#root > div > div.Dashboard_fullPage__1_NVb >"
                " div.Dashboard_main__3DhrS >"
                " div.Page_page__A7lqB.MyOrdersPage_page__12L4q.dark > div >"
                " div.Page_content__1d0Vb.MyOrdersPage_content__2BKi5 > form >"
                " div.Pagination_paginationWrapper__yuZIA.MyOrdersPage_paginationBlock__224A3.Pagination_withSelectCount__wcCl5.Pagination_dark__3k7yM"
                " > ul > li.Pagination_next__kb8bl"
            ),
        ).click()
        j += 1
        print(
            Fore.MAGENTA
            + f"\n{str(scraped_item_counter)}/{str(amount_of_items)} successfully"
            " scraped"
        )


def fill_prices():
    """
    Goes through the imported items and fills in the ebay price
    with the recommended price of the item
    """
    loop_amount = 0

    try:
        WebDriverWait(driver, timeout=500).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[3]/button[1]")
            )
        )
        loop_amount = driver.find_element(
            By.CSS_SELECTOR,
            (
                "body > div:nth-child(9) > div > div > form >"
                " div.EditProduct_content__pL_TE > div >"
                " div.TabsNav_nav__2RQ7d.EditProduct_navTabs__xt7eH.TabsNav_dark__3zunU"
                " > div.TabsNav_itemsCount__1h5NM > p > span:nth-child(2)"
            ),
        ).text
    except NoSuchElementException:
        print(ERROR_NO_ELEMENT)
    else:
        for _ in range(int(loop_amount) - 1):
            time.sleep(2)
            # Gets ebay price from box
            ebay_price = driver.find_element(
                By.CSS_SELECTOR,
                (
                    "body > div:nth-child(9) > div > div > form >"
                    " div.EditProduct_content__pL_TE > div > div.rsw_2Y >"
                    " div.rsw_2f.rsw_3G > div > div > div >"
                    " div.ProductStoreParameters_prices__OkFiY >"
                    " div.ProductStoreParameters_storesPricesBlock__28fx1 >"
                    " a:nth-child(2) > p"
                ),
            ).text
            # formats price without $
            formatted_price = ebay_price.split("$")[1]
            # gets list price box element
            list_price_box = driver.find_element(
                By.XPATH, '//*[@id="basic-details.ebay.price"]'
            )
            for _ in range(6):
                list_price_box.send_keys(Keys.BACK_SPACE)
            time.sleep(1)
            for _, char in enumerate(formatted_price):
                time.sleep(0.1)
                list_price_box.send_keys(char)

            time.sleep(1)
            # blank space
            driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[2]"
            ).click()
            time.sleep(1)
            # next button
            driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[3]/button[3]"
            ).click()


def wait_for_first_image():
    # finding first listing product image
    WebDriverWait(driver, timeout=50000).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.ImportListPage_page__2TVxh.dark > div > div.Page_content__1d0Vb.ImportListPage_content__1ZKal > form > div.ProductsFormContent_productsWrapper__38CQo.ImportListPage_itemsListWrapper__1W-c9 > div > div:nth-child(1) > div > div.ImportListItem_leftPart__1MYAn > div.Picture_pictureWrapper__vVM0a.ImportListItem_imageWrapper__10rIC",
            )
        )
    )


def fill_price_from_csv():
    """
    Goes through the imported items and fills in the ebay price
    with the price of the item from the CSV file.
    Format for CSV:
        Product Name, Quantity, Retail Price, Received, Profit, Amazon Link, and Ebay Link
    """

    # change path to relative
    csv_file = pandas.read_csv("all_products.csv")

    loop_amount = 0

    # while next button is visible
    while True:
        try:
            # finding first listing product image
            WebDriverWait(driver, timeout=50000).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "#root > div > div.Dashboard_fullPage__1_NVb > div.Dashboard_main__3DhrS > div.Page_page__A7lqB.ImportListPage_page__2TVxh.dark > div > div.Page_content__1d0Vb.ImportListPage_content__1ZKal > form > div.ProductsFormContent_productsWrapper__38CQo.ImportListPage_itemsListWrapper__1W-c9 > div > div:nth-child(1) > div > div.ImportListItem_leftPart__1MYAn > div.Picture_pictureWrapper__vVM0a.ImportListItem_imageWrapper__10rIC",
                    )
                )
            )
        except NoSuchElementException:
            print(ERROR_NO_ELEMENT)

        # finding the "select all" items checkbox
        driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[1]/div/div[1]/label',
        ).click()
        # clicking the "Post" button
        driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[1]/div[2]/div[2]/div/div[4]',
        ).click()
        time.sleep(1)
        # clicking the "Post to eBay" button
        driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[1]/div[2]/div[2]/div/div[4]/div[2]/div[1]',
        ).click()

        # Select all items checkbox
        # driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[1]/div/div[1]/label').click()

        try:
            WebDriverWait(driver, timeout=50000).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[3]/button[1]")
                )
            )
            loop_amount = driver.find_element(
                By.CSS_SELECTOR,
                (
                    "body > div:nth-child(9) > div > div > form >"
                    " div.EditProduct_content__pL_TE > div >"
                    " div.TabsNav_nav__2RQ7d.EditProduct_navTabs__xt7eH.TabsNav_dark__3zunU"
                    " > div.TabsNav_itemsCount__1h5NM > p > span:nth-child(2)"
                ),
            ).text
        except NoSuchElementException:
            print(ERROR_NO_ELEMENT)

        for _ in range(int(loop_amount) - 1):
            try:
                time.sleep(1)
                category = driver.find_element(
                    By.CSS_SELECTOR, "#basic-details\.ebay\.category"
                ).get_attribute("value")
                if category == "":
                    profit_box = driver.find_element(
                        By.XPATH, '//*[@id="basic-details.ebay.profit"]'
                    )
                    # delete price in list price box
                    for _ in range(6):
                        profit_box.send_keys(Keys.BACK_SPACE)
                    time.sleep(1)

                    # input negative value to list price box
                    profit_box.send_keys("0.10")

                    time.sleep(1)
                    # blank space
                    driver.find_element(
                        By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[2]"
                    ).click()
                    time.sleep(1)
                    # next button
                    driver.find_element(
                        By.XPATH,
                        "/html/body/div[2]/div/div/form/div[2]/div[3]/button[3]",
                    ).click()
                    continue

                product_name = driver.find_element(
                    By.CSS_SELECTOR, "#basic-details\.ebay\.name"
                ).get_attribute("value")
                product_received_price = 0
                product_input_price = 0
                product = csv_file.loc[
                    csv_file["Product Name"].str.contains(product_name, regex=False)
                ]

                if not product.empty:
                    row_number = product.index
                    product_received_price = product.loc[row_number, "Received"].values[
                        0
                    ]
                    product_quantity = product.loc[row_number, "Quantity"].values[0]
                    product_input_price = str(
                        round(product_received_price / product_quantity, 2)
                    )
                    list_price_box = driver.find_element(
                        By.XPATH, '//*[@id="basic-details.ebay.price"]'
                    )
                    for _ in range(6):
                        list_price_box.send_keys(Keys.BACK_SPACE)
                    time.sleep(1)
                    for _, price in enumerate(product_input_price):
                        time.sleep(0.1)
                        list_price_box.send_keys(price)

                    time.sleep(1)
                    # blank space
                    driver.find_element(
                        By.XPATH, "/html/body/div[2]/div/div/form/div[2]/div[2]"
                    ).click()
                    time.sleep(1)
                    # next button
                    driver.find_element(
                        By.XPATH,
                        "/html/body/div[2]/div/div/form/div[2]/div[3]/button[3]",
                    ).click()
                else:
                    driver.find_element(
                        By.XPATH,
                        "/html/body/div[2]/div/div/form/div[2]/div[3]/button[3]",
                    ).click()
                    continue
            except NoSuchElementException:
                print(ERROR_NO_ELEMENT)
                continue
        # clicking on the exit dialog button
        driver.find_element(By.XPATH, "/html/body/div[2]/div/div/button").click()
        time.sleep(2)
        # clicking on the next page button
        if (
            driver.find_element(By.CLASS_NAME, "Pagination_next__kb8bl").is_enabled()
            is False
        ):
            break
        driver.find_element(By.CLASS_NAME, "Pagination_next__kb8bl").click()


def remove_bad_products():
    """
    Removes items from the import list that are VERO, failed to list, restricted by eBay,
    below 0.9 profit, or have a negative profit amount.
    """

    items_clicked = 0
    profit_amount = 0.8
    time.sleep(2)

    pages = driver.find_elements(By.CLASS_NAME, "Pagination_page__1vJsU")
    pages[-1].click()

    while True:
        try:
            wait_for_first_image()
        except NoSuchElementException:
            print(ERROR_NO_ELEMENT)

        item_cards = driver.find_elements(
            By.CLASS_NAME, "ImportListItem_itemContainer__Wsg7n"
        )

        # finds items with vero message or negative profit and selects thems
        for i, card in enumerate(item_cards):
            index = i + 1
            try:
                has_vero_message = card.find_elements(
                    By.CLASS_NAME, "ImportListItem_veroMessage__cdkzG"
                )
                price = card.find_element(
                    By.XPATH, f'//*[@id="products[{i}].profits[0]"]'
                ).get_attribute("value")

                has_failed_posting = card.find_elements(
                    By.CLASS_NAME, "StoreBox_fail__2AWFA"
                )

                if (
                    len(has_vero_message) > 0
                    or len(has_failed_posting) > 0
                    or price[:1] == "-"
                    or float(price) < profit_amount
                ):
                    driver.find_element(
                        By.XPATH,
                        f'//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[3]/div/div[{index}]/div/div[1]/label',
                    ).click()
                    items_clicked += 1
            except NoSuchElementException:
                continue

        # deletes selected items
        if items_clicked > 0:
            time.sleep(2)
            driver.find_element(
                By.XPATH,
                '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[1]/div/div[1]/div/div/div[1]',
            ).click()
            time.sleep(2)
            driver.find_element(
                By.XPATH,
                '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/form/div[1]/div/div[1]/div/div/div[2]/div[2]',
            ).click()
            time.sleep(2)
            driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div/div[2]/button[2]"
            ).click()
        if has_prev_page():
            click_prev_page_button()
        else:
            break

    driver.refresh()
    print(Fore.MAGENTA + f"{items_clicked} items were removed")


def import_amazon_links():
    """
    Imports amazon links from the CSV into the imported items list
    Format for csv:
        Product Name, Quantity, Retail Price, Received, Profit, Amazon Link, and Ebay Link
    """
    rows_read = 0
    with open("all_products.csv", "r", newline="", encoding="utf-8") as file:
        # Gets all rows from the csv into an array
        links = []
        reader = csv.DictReader(file)
        for row in reader:
            links.append(row.get("Amazon Link", None))

        # Goes through list of rows (50 at a time) and imports them into the website
        for _ in range(len(links)):
            if rows_read >= len(links):
                print(Fore.GREEN + "All links have been successfully imported")
                break
            # Waits for "Add product manually" button to be clickable
            try:
                WebDriverWait(driver, timeout=50000).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[1]/div/div[1]/button',
                        )
                    )
                )
            except NoSuchElementException:
                print(ERROR_NO_ELEMENT)

            # clicks "Add product manually" button
            driver.find_element(
                By.XPATH,
                '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[1]/div/div[1]/button',
            ).click()

            # Waits for "Add" button in import dialog to be clickable
            try:
                WebDriverWait(driver, timeout=50000).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "/html/body/div[2]/div/div/form/div/div[2]/button",
                        )
                    )
                )
            except NoSuchElementException:
                print(ERROR_NO_ELEMENT)
            # creates a str of links from array[n, n+50] then imports them
            links_str = "\n".join(links[rows_read : rows_read + 50])
            driver.find_element(By.ID, "productLink").send_keys(links_str)
            time.sleep(2)
            driver.find_element(
                By.XPATH, "/html/body/div[2]/div/div/form/div/div[2]/button"
            ).click()
            rows_read = rows_read + 50


def scrape_and_import():
    """
    Scrapes products and then imports the amazon links into the import list
    """
    scrape_items()
    driver.get(IMPORT_LIST_LINK)
    import_amazon_links()


# User input to start module
valid_options = ["1", "2", "3", "4", "5", "end"]
USER_INPUT = ""
while USER_INPUT not in valid_options:
    print(Fore.GREEN + "\nWelcome to a dropshipping All-In-One Tool!\n")
    print(
        Fore.YELLOW
        + "1. Item Scraper\n2. Price Filler\n3. Price Filler From CSV\n4. Remove Bad"
        " Products\n5. Import Amazon Links From CSV\n6. Item Scraper + Import Amazon Links"
    )
    USER_INPUT = input("\nSelect which module you want to use (type 'end' to stop): ")

    if USER_INPUT == "1":
        scrape_items()
    elif USER_INPUT == "2":
        fill_prices()
    elif USER_INPUT == "3":
        fill_price_from_csv()
    elif USER_INPUT == "4":
        remove_bad_products()
    elif USER_INPUT == "5":
        import_amazon_links()
    elif USER_INPUT == "6":
        scrape_and_import()
    elif USER_INPUT == "7":
        # click_prev_page_button()
        click_prev_page_button()
    elif USER_INPUT == "end":
        break
    else:
        print(Fore.RED + "Invalid input. Please select another option.")
