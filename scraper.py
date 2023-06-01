from serpapi import GoogleSearch
import os, json
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

params = {
    # https://docs.python.org/3/library/os.html#os.getenv
    'api_key': os.getenv('API_KEY'),    # your serpapi key
    'engine': 'home_depot',             # SerpApi search engine
    'q': 'barbeque machine',    	        # query
}

search = GoogleSearch(params)           # where data extraction happens on the SerpApi backend
results = search.get_dict()             # JSON -> Python dict


product_ids = [result['product_id'] for result in results['products']]

home_depot_products = []

for product_id in product_ids:
    product_params = {
        # https://docs.python.org/3/library/os.html#os.getenv
        'api_key': os.getenv('API_KEY'),    # your serpapi key
        'engine': 'home_depot_product',     # SerpApi search engine
        'product_id': product_id,           # HomeDepot ID of a product
    }

    product_search = GoogleSearch(product_params)
    product_results = product_search.get_dict()

    home_depot_products.append(product_results['product_results'])


def get_information():
    info = " "
    for i in range(3):
        info += "--------"\
            "Title: " + str(home_depot_products[i]['title']) + " Description: " + str(home_depot_products[i]['description']) +\
               " Rating: " + str(home_depot_products[i]['rating']) + " Reviews: " + str(home_depot_products[0]['reviews']) +\
               " Price: " + str(home_depot_products[i]['price']) + " Link: " + str(home_depot_products[i]['info_and_guides']) +\
               " Highlights: " + str(home_depot_products[i]['highlights']) + " Brand : " + str(home_depot_products[i]['brand']) +\
               " Bullets: " + str(home_depot_products[i]['bullets']) + " Specifications : " + str(home_depot_products[i]['specifications']) +\
               "--------"

    return info

