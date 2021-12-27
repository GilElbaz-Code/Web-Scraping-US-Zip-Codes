import pandas as pd
import requests


def get_api_call():
    """
       get_api_call gets the GET response from the web archives server using CDX API
       :return: CDX API output in json format.
    """
    craig_list = 'https://chicago.craigslist.org/d/musical-instruments/search/msa'
    url = 'https://web.archive.org/cdx/search/cdx?url=' + craig_list + '&fl=timestamp,original&output=json'
    api_request = requests.get(url)
    api_output = api_request.json()
    return api_output


def create_table(data):
    """
        create_table takes the json output from te get_api_function and returns Pandas Dataframe.
        :param data: the json file from get_api_call function.
        :return: proper Pandas dataframe which contains:
         1) Data Date Point
         2) URL
    """
    columns = ['Data_Date_Point', 'URL']
    df = pd.DataFrame(data, columns=columns)
    df.drop(index=df.index[0], axis=0, inplace=True)
    print(df)


if __name__ == '__main__':
    api_data = get_api_call()
    create_table(api_data)
