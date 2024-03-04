"""
Huai-An Tseng 
Class: CS 521 - Spring 1 
Date: March 2 
Link to DEMO: https://youtu.be/YhMki09H3d4
Final Project - Lululemon WMTM Scraper
This web scraping program collect items information
from Lululemon We Made Too Much(WMTM) webpage, export as a csv file. Based
on user input, find the item of desired.

How to use this program:
This program ask if user want to load the latest sale item list from
lululemon. If press Y, it takes 5 minutes to scrapes data from chome page,
if press other, it skip scraping and directly search sale items from
pre-load sale-item csv for items match key words. 

This file includes:
CSV Export, Read and Search Functionality, search products for users:
"""
from data import Data
import csv

csv_file_path = "/Users/irenetseng/Desktop/BU_CS521/anntseng_final_project/" \
                "Final Project_Huai-An_Tseng/lulu_WMTM.csv"


def export_dict(data: dict, csv_file_path=csv_file_path):
    """ Export the WMRM_dict to csv file. """
    with open(csv_file_path, 'w', newline='') as csv_file:
        fieldnames = ['Product Name', 'Sale Price']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for k, v in data.items():
            csv_row = {}
            csv_row[fieldnames[0]] = k  # Set 'Product Name'
            csv_row[fieldnames[1]] = v  # Set 'Sale Price'
            writer.writerow(csv_row)
    print('original data:')
    print(data)
    print("Data stored to csv file!")


def read_csv(csv_file_path=csv_file_path):
    """ Read content from csv file and return a dictionary. """
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headings = next(csv_reader)
        print('Reading csv file:')
        data = {}
        for line in csv_reader:
            data[line[0]] = line[1]
        print(data)
        return data


def search_desired_item(user_input: str, product_dict: dict):
    """ This function take user_inpu keyword and return all items contains
    the keyword in the product name as a set."""
    print("Let's search your item: ", user_input)
    sale_items = set()
    for key, value in product_dict.items():
        if user_input.lower() in key.lower():
            sale_items.add(
                (key, value))  # store key, value as tuple in the set
    if len(sale_items) == 0:
        print(f"Itme Not Found! Key words: {user_input}")
    else:
        print(f"Good New! items are on sale! Key words: {user_input}")
        for index, item in zip(range(1, 500), sale_items):
            print(f'{index}. Product Name: {item[0]} Sale Price: {item[1]}')
    return sale_items


if __name__ == '__main__':
    """Ask if user want to do web scraping or read from current csv, 
    then search sale items using desired key words."""
    user_reload_data = input("Do you want to scrape the latest sale items "
                             "from Lululemon website or use a CSV file from "
                             "a previous session? \nkey in 'Y' to load or "
                             "any other to skip and search items: ")
    if user_reload_data == "Y" or user_reload_data == "y":
        print("start loading on sale item data from lululemon! ")
        lulu_data = Data()
        products = lulu_data.lulu_wmtm_scraper()
        print("tart exporting data to csv file...")

        """unit test 1, test if the url getter method return correct url 
        string."""
        url = lulu_data.get_url()
        assert url == "https://shop.lululemon.com/c/sale/_/N-1z0xcuuZ8t6"

    read_product = read_csv()
    # while True: # constantly ask user and search for items.
    #     try:
    #         user_input = input("Please key in the keyword of your desired "
    #                            "product:")
    #         search_desired_item(user_input, read_product)
    #     except Exception as e:
    #         print(e)
    #         continue

    """ unit test 2, test if the uer_input key word is in the result. 
    We searched for "Hoodie", convert the returned set to list so it support 
    indexing. Then check the first product name has "Hoodie" in it. """
    search_result_set = search_desired_item("Hoodie", read_product)
    assert "Hoodie" in list(search_result_set)[0][0]
