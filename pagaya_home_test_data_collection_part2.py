import requests
import pandas as pd
import concurrent.futures
import zc_list

MAX_THREADS = 50
headers = {'User-Agent': 'Chrome/50.0.2661.102'}


def set_first_row_as_header(df):
    new_header = df.iloc[0]  # grab the first row for the header
    df = df[1:]  # take the data less the header row
    df.columns = new_header  # set the header row as the df header
    return df


def get_population_gender_percent(zipcode):
    url = f'https://www.unitedstateszipcodes.org/{zipcode}'
    page = requests.get(url, headers=headers)
    df_list = pd.read_html(page.text)  # this parses all the tables in webpages to a list
    population_df = df_list[1]

    # Handling gender and percent
    gender_percent = df_list[6]
    gender_percent.drop(gender_percent.columns[1], axis=1, inplace=True)
    gender_percent = gender_percent.transpose().reset_index(drop=True)
    gender_percent = set_first_row_as_header(gender_percent)

    # Handling population value
    population = population_df.iloc[:1]
    population = population.dropna(axis=1).transpose()
    population = set_first_row_as_header(population)

    frames = [population, gender_percent]
    combined = pd.concat(frames, axis=1, join='inner')
    combined.insert(0, 'ZIP Code', zipcode)
    return combined


def get_stats(zipcodes):
    threads = min(MAX_THREADS, len(zipcodes))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_population_gender_percent, zipcodes)


if __name__ == '__main__':
    all_zip_codes = zc_list.get_zipcode_list()
    df_combined = get_stats(all_zip_codes)
    print(df_combined)
