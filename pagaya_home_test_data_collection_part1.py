import requests
import pandas as pd
import re, json
import concurrent.futures
import zc_list

MAX_THREADS = 50

zip_to_coords = {}


def request_zipcode(code):
    global zip_to_coords
    results = []
    columns = ["ZIP Code"]
    with requests.Session() as s:
        s.headers = {'User-Agent': 'Mozilla/5.0'}
        url = f'https://www.unitedstateszipcodes.org/{str(code).zfill(5)}/#stats'
        r = s.get(url)
        res = re.findall(r'var data = (\[.*\])', r.text)
        relevant = [data for data in res if json.loads(data)[0]["values"][0]["x"] == 2005]
        if len(relevant) > 0:
            relevant = json.loads(relevant[0])[0]["values"]
            try:
                data = relevant
                values = [i['y'] for i in data]
                values.insert(0, code)
                results.append(values)
                if values:
                    columns.extend([i['x'] for i in data])
                zip_to_coords[code] = (columns, *results)
                # print(f"{code}={zip_to_coords[code]}")
            except:
                pass
        else:
            zip_to_coords[code] = None


def get_zipcode_data(zipcodes):
    threads = min(MAX_THREADS, len(zipcodes))

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(request_zipcode, zipcodes)


if __name__ == '__main__':
    all_zip_codes = zc_list.get_zipcode_list()
    df = pd.DataFrame(get_zipcode_data(all_zip_codes))
    print(df)
