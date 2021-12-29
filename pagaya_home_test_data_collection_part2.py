import requests
import pandas as pd
import concurrent.futures
import zc_list
from bs4 import BeautifulSoup


MAX_THREADS = 50


def get_population(zipcode):
    url = f'https://www.unitedstateszipcodes.org/{zipcode}'
    headers = {'User-Agent': 'Chrome/50.0.2661.102'}
    page = requests.get(url, headers=headers)
    df_list = pd.read_html(page.text)  # this parses all the tables in webpages to a list
    population_df = df_list[1]
    gender_percent_df = df_list[6]
    population = population_df.iloc[:1].squeeze(axis=1)
    combined = pd.concat(gender_percent_df, population)
    print(combined)

def get_zipcode_data(zipcodes):
    threads = min(MAX_THREADS, len(zipcodes))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_population, zipcodes)


if __name__ == '__main__':
    get_population(23022)
    #all_zip_codes = zc_list.get_zipcode_list()
    #df = pd.DataFrame(get_zipcode_data(all_zip_codes))
    #print(df)
