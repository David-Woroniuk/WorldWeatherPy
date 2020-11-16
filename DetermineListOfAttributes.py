import urllib
import urllib.parse
import urllib.request
import json
import pandas as pd
from datetime import datetime
import os

class DetermineListOfAttributes(object):
  '''
  This class determines the list of historical weather attributes available for
  extraction by the WorldWeatherOnline API. Each of these attributes can be extracted
  using the 'retrieve_hist_data' function of the RetrieveByAttribute class separately,
  or within a list.

  -------------------------------Arguments------------------------------------------- 

  api_key: the API key obtained from 'https://www.worldweatheronline.com/developer/'. (str)
  verbose: boolean determining printing during data extraction. (bool)

  -------------------------------Returns--------------------------------------------- 

  attribute_list: a list of attributes which are available from the WWO API. (list)

  '''

  def __init__(self, api_key, verbose):

    if isinstance(api_key, str) is False:
      raise TypeError("The 'api_key' argument must be a string object. \n Please refer to https://www.worldweatheronline.com/developer/ to generate an API key.")

    if isinstance(verbose, bool) is False:
      raise TypeError("The 'verbose argument must be a boolean object.")

    self.api_key = api_key
    self.verbose = verbose

  def retrieve_list_of_options(self):
    '''
    This function enables retrieval of 'attribute_list', which contains all
    available attributes which can be retrieved from the WorldWeatherOnline API.
    '''

    attribute_list = []

    if self.verbose:
      print('Retrieving attribute list...')

    url_page = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=' + self.api_key + '&q=London&format=json&date=2020-01-01&enddate=2020-01-02&tp=1'
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


if __name__ == '__main__':   
  attributes = DetermineListOfAttributes('YOUR API KEY HERE', True).retrieve_list_of_options()
