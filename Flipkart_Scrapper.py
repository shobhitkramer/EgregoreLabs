import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from random import randint

# NumPy arrays storing the number of pages in the required search page
page_num = np.arange(1, 24, 1)
titles = []

for num in page_num:
    # accessing pages one by one by updating page parameter in url
    url = "https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&as-pos=1&as-type=RECENT&suggestionId=laptop%7CLaptops&requestId=d43410e6-39b0-4ec5-b13f-bcd0854c005c&as-backfill=on&page=" + str(
        num)
    results = requests.get(url)

    # parsing the webpage into readable HTML format
    soup = BeautifulSoup(results.text, 'html.parser')

    # this variable contains all the required div tags
    name_divs = soup.find_all('div', class_='_3wU53n')

    # generating random requests to server so as not to overwhelm it
    sleep(randint(2, 10))

    for container in name_divs:
        titles.append(container.text)

products_name = pd.DataFrame({
    'ProductName': titles
})

products_name.to_csv('laptop.csv')
