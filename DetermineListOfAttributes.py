import urllib
import urllib.parse
import urllib.request
import json
import pandas as pd
from typing import List


class DetermineListOfAttributes(object):
    """
    This class determines the list of historical weather attributes available for
    extraction by the WorldWeatherOnline API. Each of these attributes can be extracted
    using the 'retrieve_hist_data' function of the RetrieveByAttribute class separately,
    or within a list.

    :param api_key: the API key obtained from 'https://www.worldweatheronline.com/developer/'. (str)
    :param city_name: the name of the city in which the user is interested in retrieving fields. (str)
    :param date: the start date on which the user is interested in retrieving fields. (str)
    :param verbose: boolean determining printing during data extraction. (bool)
    :return: attribute_list: a list of attributes which are available from the WWO API. (list)
    """

    def __init__(self, api_key: str, city_name: str, date: str, verbose):
        if not isinstance(verbose, bool):
            raise TypeError("The 'verbose' argument must be a boolean type.")
        if verbose:
            print("Checking if input arguments are in the correct format.")
        if not all(isinstance(v, str) for v in [api_key, city_name, date]):
            raise TypeError("The 'api_key', 'city_name' and 'date' arguments must all be string types.")
        if len(api_key) != 31:
            raise ValueError("The 'api_key' argument must be a 31 digit string object. \n "
                             "Please refer to https://www.worldweatheronline.com/developer/ to generate an API key.")
        if "-" not in date:
            raise KeyError("The 'date' string must be of the format 'YYYY-MM-DD'.")
        if "/" in date:
            raise KeyError("The 'date' string must be of the format 'YYYY-MM-DD'.")

        self.api_key = api_key
        self.city_name = city_name
        self.date = date
        self.verbose = verbose

    def retrieve_list_of_options(self) -> List[str]:
        """
        This function enables retrieval of 'attribute_list', which contains all
        available attributes which can be retrieved from the WorldWeatherOnline API.
        """
        attribute_list = []
        if self.verbose:
            print('Retrieving attribute list...')

            url_page = 'http://api.worldweatheronline.com/premium/v1/past-weather.' \
                       'ashx?key={}&q={}&format=json&date=2011-01-01&enddate={}&tp=1'.format(self.api_key,
                                                                                             self.city_name,
                                                                                             self.date)
            json_page = urllib.request.urlopen(url_page, timeout=10)
            json_data = json.loads(json_page.read().decode())
            data = json_data['data']['weather']
            astronomy_data = pd.DataFrame(data[1]['astronomy'])
            hourly_data = pd.DataFrame(data[1]['hourly'])

            for key in astronomy_data.keys():
                attribute_list.append(key)
            for key in hourly_data.keys():
                attribute_list.append(key)

            if self.verbose:
                print('List of available weather attributes: {}'.format(attribute_list))

            return attribute_list
