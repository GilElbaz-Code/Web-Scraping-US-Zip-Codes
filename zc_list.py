from bs4 import BeautifulSoup
import requests

url = 'https://www.unitedstateszipcodes.org'
headers = {'User-Agent': 'Chrome/50.0.2661.102'}
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.text, 'html.parser')

hrefs = []
all_zipcodes = []

for data in soup.find_all('div', class_='state-list'):
    for a in data.find_all('a'):
        if a is not None:
            hrefs.append(a.get('href'))
hrefs.remove(None)


def get_zipcode_list():
    for state in hrefs:
        state_url = url + state
        state_page = requests.get(state_url, headers=headers)
        states_soup = BeautifulSoup(state_page.text, 'html.parser')
        div = states_soup.find(class_='list-group')
        for a in div.findAll('a'):
            if str(a.string).isdigit():
                all_zipcodes.append(a.string)
    return all_zipcodes


