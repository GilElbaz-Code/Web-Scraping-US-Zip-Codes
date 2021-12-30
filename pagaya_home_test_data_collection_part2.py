import requests
import pandas as pd
import concurrent.futures
import zc_list

MAX_THREADS = 100
DATAFRAME_LIST = []
headers = {'User-Agent': 'Chrome/50.0.2661.102'}


def set_first_row_as_header(df):
    """
        set_first_row_as_header takes the first row of dataframe and puts it as header
        :param df: the dataframe to set its headers.
        :return: dataframe with labeled column names.
    """
    new_header = df.iloc[0]  # grab the first row for the header
    df = df[1:]  # take the data less the header row
    df.columns = new_header  # set the header row as the df header
    return df


def get_population_gender_percent(zipcode):
    """
        get_population_gender_percent scrapes population and percent by gender data and parses it
        for each zipcode a Pandas dataframe is made and appended into a list to later be combined.
        :param zipcode: zipcode for the current country.
    """
    url = f'https://www.unitedstateszipcodes.org/{zipcode}'
    page = requests.get(url, headers=headers)
    df_list = pd.read_html(page.text)  # this parses all the tables in webpages to a list
    population_df = df_list[1]

    # Handling gender and percent
    gender_percent = df_list[6]
    gender_percent.drop(gender_percent.columns[1], axis=1, inplace=True)
    gender_percent = gender_percent.transpose().reset_index(drop=True)
    gender_percent = set_first_row_as_header(gender_percent)
    gender_percent.replace('&percnt', '%', regex=True, inplace=True)

    # Handling population value
    population = population_df.iloc[:1]
    population = population.dropna(axis=1).transpose()
    population = set_first_row_as_header(population)

    frames = [population, gender_percent]
    combined = pd.concat(frames, axis=1, join='inner')
    combined.insert(0, 'ZIP Code', zipcode)
    DATAFRAME_LIST.append(combined)


def get_stats(zipcodes):
    """
        get_stats uses concurrent.futuresmodule provides a high-level interface for
        asynchronously executing callables.
        The asynchronous execution is performed with threads to allow scalability and speed
        :param zipcodes: an iterable (list) of all the zipcodes to be performed by get_population_gender_percent.
        """
    threads = min(MAX_THREADS, len(zipcodes))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_population_gender_percent, zipcodes)


if __name__ == '__main__':
    # Get all the zip code in a list
    all_zip_codes = zc_list.get_zipcode_list()
    # Scrap all the required data
    get_stats(all_zip_codes)
    # Combined all Pandas dataframe into one table.
    result_df = pd.concat(DATAFRAME_LIST, axis=0, join='inner').reset_index(drop=True)
    # print(result_df)
