import requests
import re, json
import pandas as pd
import concurrent.futures
import zc_list

MAX_THREADS = 100
headers = {'User-Agent': 'Chrome/50.0.2661.102'}

zip_to_coords = {}


def get_stats_from_graph(code):
    """
        get_stats_from_graph gets all the relevant data as required from the page and creates dictionary
        of zip code and value for each year.
        :param code: the zipcode
    """
    global zip_to_coords
    clmns = []
    with requests.Session() as s:
        s.headers = headers
        url = f'https://www.unitedstateszipcodes.org/{str(code).zfill(5)}/#stats'
        r = s.get(url)
        res = re.findall(r'var data = (\[.*\])', r.text)
        relevant = [data for data in res if json.loads(data)[0]["values"][0]["x"] == 2005]
        if len(relevant) > 0:
            relevant = json.loads(relevant[0])[0]["values"]
            try:
                data = relevant
                values = [i['y'] for i in data]
                if values:
                    clmns.extend([i['x'] for i in data])
                zip_to_coords[code] = values
            except:
                pass
        else:
            zip_to_coords[code] = None


def get_zipcode_data(zipcodes):
    """
        get_stats uses concurrent.futuresmodule provides a high-level interface for
        asynchronously executing callables.
        The asynchronous execution is performed with threads to allow scalability and speed
        :param zipcodes: an iterable (list) of all the zipcodes to be performed by get_population_gender_percent.
    """
    threads = min(MAX_THREADS, len(zipcodes))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(get_stats_from_graph, zipcodes)


if __name__ == '__main__':
    all_zip_codes = zc_list.get_zipcode_list()
    get_zipcode_data(all_zip_codes)
    df_values = [[key] + val for key, val in zip_to_coords.items()]
    columns = ["ZIP Codes", (*["Historical " + str(year) for year in range(2005, 2019)])]
    result_df = pd.DataFrame(df_values)
    result_df.columns = columns
    print(result_df)

