import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from time import sleep
from random import randint

titles = []
years = []
time = []
imdb_ratings = []
metascores = []
# To get movie titles in ENG
header = {"Accept-Language": "en-US, en;q=0.5"}

pages = np.arange(1, 1001, 50)

for page in pages:

    url = "https://www.imdb.com/search/title/?groups=top_1000&start=" + str(page) + "&ref_=adv_nxt"
    # making a request to the given URL which returns the html page
    results = get(url, headers=header)

    soup = BeautifulSoup(results.text, "html.parser")
    movie_divs = soup.find_all('div', class_='lister-item mode-advanced')

    sleep(randint(2, 10))

    for container in movie_divs:
        name = container.h3.a.text
        titles.append(name)

        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

        runtime = container.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else ''
        time.append(runtime)

        rating = float(container.strong.text)
        imdb_ratings.append(rating)

        meta = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '_'
        metascores.append(meta)

# pandas Dataframe
movies = pd.DataFrame({
    'Movie': titles,
    'Year': years,
    'TimeMin': time,
    'IMDB': imdb_ratings,
    'Metascore': metascores
})

# cleaning data
movies['Year'] = movies['Year'].str.extract('(\d+)').astype(int)
movies['TimeMin'] = movies['TimeMin'].str.extract('(\d+)').astype(int)

# Generating a CSV

movies.to_csv('movies.csv')
