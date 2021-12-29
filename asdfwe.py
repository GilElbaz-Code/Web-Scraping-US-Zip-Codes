import requests
from bs4 import BeautifulSoup
import pandas as pd
import re, json

'''
1) Fetch all the US zipcodes and put into a list
2) Use BS with requests to fetch each graph and store it (how?)
'''
results = []
columns = ['zip']

with requests.Session() as s:
    s.headers = {'User-Agent': 'Mozilla/5.0'}

    for code in range(23022, 23023):

        url = f'https://www.unitedstateszipcodes.org/{code}/#stats'
        r = s.get(url)

        try:
            res = re.findall(r'var data = (\[.*\])', r.text)
            relevant = [data for data in res if json.loads(data)[0]["values"][0]["x"] == 2005][0]
            print(relevant)
            values = [i['y'] for i in relevant]
            values.insert(0, code)
            results.append(values)

            if values and len(columns) == 1:
                columns.extend([i['x'] for i in relevant])
        except:
            pass

pd.options.display.max_columns = None








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
