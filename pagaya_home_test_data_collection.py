import requests
import pandas as pd
from bs4 import BeautifulSoup
import calendar
import datetime

'''
1) Extract data from web. - Hard
2) Insertion to Pandas dataframe. - Easy
'''

url = 'https://www.unitedstateszipcodes.org/23022/#stats'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/50.0.2661.102 Safari/537.36'}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())


years = ['Historical ' + str(year) for year in range(2005, 2019)]

columns = ['ZIP Code', 'Current Population', *years]
df = pd.DataFrame(columns=columns)
print(df)

if __name__ == '__main__':
    pass
