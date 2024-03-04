"""
Huai-An Tseng 
Class: CS 521 - Spring 1 
Date: March 2 
Final Project - Lululemon WMTM Scraper
This web scraping program collect items information
from Lululemon We Made Too Much(WMTM) webpage, export as a csv file. Based
on user input, find the item of desired.

How to use this program:
This program ask if user want to load the latest sale item list from
lululemon. If press Y, it takes 5 minutes to scrapes data from chome page,
if press other, it skips scraping and directly search sale items from
preloaded sale-item csv for items match key words.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By # serch htnk element by its id, 
# class name ...etc
import time

class Data:
    """
    The Data class will present a list of items scraped from Lululemon We 
    Made Too Much webpage
    """
    def __init__(self, url="https://shop.lululemon.com/c/sale/_/N-1z0xcuuZ8t6"):
        self._lulu_WMTM_url = url
        self._load_btn_class_name = "pagination_button__V8a85"
        self._product_list_class_name = "product-list_productListItem__uA9Id"
        self._automate_chrome()
        self.url = self.get_url()
        self._driver = None
        self.product_dict = None

    def get_url(self):
        """ A getter function simply return url."""
        return self._lulu_WMTM_url

    def _automate_chrome(self):
        """
        Build an automation tool using selenium that controls chrome.
        Connect selenium to chromedriver.exe folder located in same directory.
        """
        chrome_driver_path = "/Users/irenetseng/Desktop/BU_CS521" \
                             "/anntseng_final_project/Final " \
                             "Project_Huai-An_Tseng/chromedriver"
        service = Service(executable_path=chrome_driver_path)
        self._driver = webdriver.Chrome(service=service)

    def _open_page(self):
        """ Open the web page."""
        self._driver.get(self.get_url())

    def load_data(self):
        """
        Load data, build chrome automation, open page and then load data.
        using time.sleep to make delay to insure the success of web scraping.
        """
        time.sleep(8)
        attemp = 2
        for i in range(attemp):
            print("Attemp #: ", i+1, " / ", attemp)
            try:
                load_button = self._driver\
                    .find_element(By.CLASS_NAME, self._load_btn_class_name)
                time.sleep(2)
                load_button.click()
                time.sleep(5)
                print("Attemp #: ", i+1, " -- Success")
            except Exception as e:
                print("Attemp #: ", i+1, " -- Failed")
                print(e)
        try:
            products = [product.text for product in self._driver.find_elements(
                By.CLASS_NAME, self._product_list_class_name)]
            print("Get whole product information.....")
            print(products)
            print(len(products))
        except Exception as e:
            print("Get whole product info Failed!")
            print(e)
        else:
            print("Get item information successfully!")
        self.product_dict = products
        return products

    def _close_page(self):
        """ Close page of designated url. """
        print("Close page")
        self._driver.quit()  # close the window.
    
    def lulu_wmtm_scraper(self):
        """
        This function return a dictionary of current sale items on lululemon 
        WMTM webpage and related price.
        """
        # Create new Data class instance, get product list
        self._automate_chrome()
        self._open_page()
        products = self.load_data()
        # Eliminate items that's not sale products.
        products = [p for p in products if "Sale Price" in p]
        self._close_page()

        # Put all accessed sale item, and build a dictionary
        WMTM_dict = dict()
        # for i, p in zip(range(1, 500), products):
        for p in products:
            product_name = p.split("\nSale Price \n")[0].replace('\n', '')
            product_sale_price = p.split("\nSale Price \n")[1].split(
                "\nRegular Price")[0]
            WMTM_dict[product_name] = product_sale_price
        print("Your WMTM dictionary is created!")
        return WMTM_dict
    
    def __repr__(self) -> str:
        return "LULULEMON WE MADE TOO MUCH: " + " ".join([i for i in
                                                          self.product_dict])
    
    def __len__(self):
        return len(self.product_dict)

