import pandas as pd
import requests

'''
Please write an API call into ‘wayback machine’ which returns:
1) How many data points we have for the URL.
please store the results in a table which has: Data point Date , URL for the data point.
'''


def get_api_call():
    craig_list = 'https://chicago.craigslist.org/d/musical-instruments/search/msa'
    url = 'https://web.archive.org/cdx/search/cdx?url=' + craig_list + '&fl=timestamp,original&output=json'
    api_request = requests.get(url)
    api_output = api_request.json()
    return api_output


def create_table():
    columns = ['Data_Date_Point', 'URL']
    df = pd.DataFrame(api_output, columns=columns)
    df.drop(index=df.index[0], axis=0, inplace=True)
    print(df)


if __name__ == '__main__':
    get_api_call()
