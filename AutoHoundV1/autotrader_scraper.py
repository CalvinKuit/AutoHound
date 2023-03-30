import requests
from bs4 import BeautifulSoup
import json
import re
import itertools
import time
import datetime
import random
import csv

request_count = 0 

# obtain last page by scraping from url given
def get_lastpage(link_url):
    global request_count
    request_count += 1
    mainresponse = requests.get(link_url)
    # print(mainresponse)
    mainsoup = BeautifulSoup(mainresponse.text, "html.parser")
    page_numbers = [item.text.strip().replace(" ","") for item in mainsoup.find_all("li", class_="e-page-number")]
    last_page = page_numbers[-1]
    return int(last_page)


#obtain car links for one page only 
def get_carlinks(url_link):
    global request_count
    request_count += 1
    url = 'https://proxy.scrapeops.io/v1/'
    params = {
        'api_key': '117dadb1-18cd-4761-a4e9-011b91e77b2d',
        'url': url_link,
    }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    link_list = []
    for div in soup.find_all("div", class_="e-available m-has-photos"):
        for a in div.find_all("a", href=True):
            link = "https://www.autotrader.co.za" + a["href"]
            link_list.append(link)

    return (link_list)


def get_all_links(url):
    last_page = get_lastpage(url)
    if "pagenumber=" in url:
        # URL contains a page number, generate list of links based on page number
        base_url = url.split("pagenumber=")[0]
        links = [f"{base_url}pagenumber={i}&priceoption=RetailPrice" for i in range(1, last_page+1)]
    else:
        # URL does not contain a page number, assume it's for the first page
        base_url = url.split("?")[0]
        links = [f"{base_url}?pagenumber={i}&priceoption=RetailPrice" for i in range(1, last_page+1)]
    return links


# returns data scraped from a single page in json format
def autotrader_data(url_link):
    global request_count
    request_count += 1
    
    url = 'https://proxy.scrapeops.io/v1/'
    params = {
        'api_key': '117dadb1-18cd-4761-a4e9-011b91e77b2d',
        'url': url_link, 
    }
    
    response = requests.get(url=url, params=params)
    
    if response.status_code == 503:
        return f"Server Unavailable"
    else:
        soup = BeautifulSoup(response.text, "html.parser")

        components = url_link.split("/")

        brand = components[4]
        model = components[5]
        spec = components[6]

        # Get the text of the h1 with class "e-listing-title"
        
        full_title = soup.find("h1", class_="e-listing-title").text.strip().replace("For Sale", "")[5:].rstrip()

        #getting the primary key
        title = soup.title.text.strip()
        id = re.search("ID: (.*) - AutoTrader", title).group(1)

        # Get the text of the div with class "e-price"
        price = soup.find("div", class_="e-price").text.strip().replace("\xa0", " ").replace("R ","").replace(" ","")

        # Get the text of all the list items with class "e-summary-icon"
        text_list = [item.text.strip().replace("\xa0", "").replace(" km","") for item in soup.find_all("li", class_="e-summary-icon")]

        car_data = {
            "id": "AT" + id,
            "make": brand,
            "model": model,
            "spec": spec,
            "full_title": full_title,
            "price": price,
            "condition": text_list[0],
            "year": text_list[1],
            "km": text_list[2],
            "transmission": text_list[3],
            "fuel_type": text_list[4],
            "source": "AutoTrader",
            "link": url_link
        }

        # Get the text of all the divs with class "col-6" within the parent div
        parent_div = soup.find("div", class_="b-striped-specs")
        col_divs = parent_div.find_all("div", class_="col-6")
        more_specs = [col_div.text for col_div in col_divs]

        # Add each 2nd item in more_specs to car_data with the specified key values
        car_data["LastUpdated"] = more_specs[1]

        return car_data

def get_all_cardata(url):
    all_pages = get_all_links(url)
    all_cars = []
    for i in all_pages:
        all_cars += get_carlinks(i)
    return all_cars

def csv_to_car_data(csv_file):
    input_file = csv_file
    data = []
    with open(input_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            id, make, model, spec, full_title, price, condition, year, km, transmission, fuel_type, source, link = row
            item = {
                "id": id,
                "make": make,
                "model": model,
                "spec": spec,
                "full_title": full_title,
                "price": price,
                "condition": condition,
                "year": year,
                "km": km,
                "transmission": transmission,
                "fuel_type": fuel_type,
                "source": source,
                "link": link
            }
            data.append(item)
    return data