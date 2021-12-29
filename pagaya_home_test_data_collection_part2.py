import requests
import pandas as pd
import concurrent.futures
import zc_list

MAX_THREADS = 50
headers = {'User-Agent': 'Chrome/50.0.2661.102'}


def get_population_gender_percent(zipcodes):
    global combined
    for zipcode in zipcodes:
        url = f'https://www.unitedstateszipcodes.org/{zipcode}'
        page = requests.get(url, headers=headers)
        df_list = pd.read_html(page.text)  # this parses all the tables in webpages to a list
        population_df = df_list[1]
        gender_percent_df = df_list[6]
        population = population_df.iloc[:1].squeeze(axis=1)
        combined = pd.concat(gender_percent_df, population)

    return combined


def get_zipcode_data(zipcodes):
    threads = min(MAX_THREADS, len(zipcodes))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_population_gender_percent, zipcodes)


if __name__ == '__main__':
    all_zip_codes = zc_list.get_zipcode_list()
    df_combined = get_population_gender_percent(all_zip_codes)
