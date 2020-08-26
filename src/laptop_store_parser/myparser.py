import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

__START_PAGE__ = 'https://komp.1k.by/mobile-notebooks/page1'
__SUCCESS_CODE__ = 200
__SINGLE_LAPTOP_CLASS_NAME__ = 'prod-nb__head'
__SINGLE_LAPTOP_IMAGE_CLASS__ = 'prod-nb__img'
__SINGLE_LAPTOP_NAME_CLASS__ = 'prod-nb__name'
__SINGLE_LAPTOP_PRICE_CLASS__ = 'prod-nb__price'
__IMAGE_LINK__ = 'image_link'
__LAPTOP_NAME__ = 'laptop_name'
__LONG_PRICE__ = 'long_price'
__LAPTOP_TABLE_PATH__ = 'data-tables/laptops1k.csv'


def get_producer_name(laptop_full_name):
    producer = None
    split_name = laptop_full_name.split()
    producer = split_name[0 if (split_name[0].lower() != 'ноутбук') else 1]
    return producer


def get_next_page_link(cur_page: str):
    # page is a key word, after which a number stands.
    # having a number, we may just add +1 to get the next page id.
    divided_link = cur_page.split('page')
    page_id = int(divided_link[1])
    return divided_link[0] + 'page' + str(int(divided_link[1]) + 1)


def get_laptop_data_from_div(div_dictionary) -> dict:
    '''
    :param div_dictionary:
    :return: dict with keys:
    "image_link" - link to download the image
    "laptop_name" - full name of the laptop
    "long_price" - scale of the price (like '205$ - 305$')
    '''
    data = {}
    data[__IMAGE_LINK__] = [div_dictionary.findAll("img", {"class": __SINGLE_LAPTOP_IMAGE_CLASS__})[0]['src']]
    long_name = div_dictionary.findAll("span", {"class": __SINGLE_LAPTOP_NAME_CLASS__})[0].text.replace('\n', '')
    data[__LAPTOP_NAME__] = [get_producer_name(long_name)]
    data[__LONG_PRICE__] = [div_dictionary.findAll("div", {"class": __SINGLE_LAPTOP_PRICE_CLASS__})[0].text]
    return data


def get_list_of_laptop_data(response):
    list_of_data = []
    soup = BeautifulSoup(response.text, "html.parser")
    # To download the whole data set, let's do a for loop through all a tags
    for one_a_tag in soup.findAll("div", {"class": __SINGLE_LAPTOP_CLASS_NAME__}):  # 'a' tags are for links
        list_of_data.append(get_laptop_data_from_div(one_a_tag))
        # download_url = 'http://web.mta.info/developers/' + link
        # urllib.request.urlretrieve(download_url, './' + link[link.find('/turnstile_') + 1:])
        # add 1 for next line
    return list_of_data


def create_csv_file(full_path):
    os.chdir('../')
    headers = pd.DataFrame({__IMAGE_LINK__: [], __LAPTOP_NAME__: [], __LONG_PRICE__: []})
    headers.to_csv(full_path, index=False)


def write_datas_to_csv(list_of_datas, path):
    for data in list_of_datas:
        pd_data = pd.DataFrame(data)
        pd_data.to_csv(path, mode='a', header=False, index=False)


def save_laptop_data_to_csv_table():
    # cur position is /src/laptop_store_parser/
    # create_csv_file(__LAPTOP_TABLE_PATH__)
    # current_page = __START_PAGE__
    # response = requests.get(current_page)
    # while response.status_code == __SUCCESS_CODE__:
    #     print('cur page=', current_page)
    #     write_datas_to_csv(get_list_of_laptop_data(response), __LAPTOP_TABLE_PATH__)
    #     current_page = get_next_page_link(current_page)
    #     response = requests.get(current_page)
    print('FINISHED!')
