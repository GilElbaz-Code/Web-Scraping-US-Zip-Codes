import requests
from bs4 import BeautifulSoup
import pandas as pd
import re, json
import threading

FIRST_ZIP_CODE = 601
LAST_ZIP_CODE = 99950

zip_to_coords = {}
threads = []


def request_zipcode(code):
    global zip_to_coords
    results = []
    columns = ["zip"]
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
                print(f"{code}={zip_to_coords[code]}")
            except:
                pass
        else:
            zip_to_coords[code] = None


for i in range(23022, 23100):
    t = threading.Thread(target=request_zipcode, args=(i,), daemon=True)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# pd.options.display.max_columns = None
# pd.options.display.max_rows = None
# df = pd.DataFrame(results, columns=columns)
# print(df)


'''
url = 'https://www.unitedstateszipcodes.org/23022/#stats'
headers = {'User-Agent': 'Chrome/50.0.2661.102'}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

links = soup.find_all('a', href=True)
'''

'''
years = ['Historical ' + str(year) for year in range(2005, 2019)]

columns = ['ZIP Code', *years]
df = pd.DataFrame(columns=columns)
print(df)
'''
if __name__ == '__main__':
    pass
