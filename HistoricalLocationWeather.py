import os
import urllib
import urllib.parse
import urllib.request
import json
import pandas as pd
from datetime import datetime


class HistoricalLocationWeather(object):
    """
    This class extracts Historical weather characteristics for a number of
    predefined features from the WorldWeatherOnline API. The data is extracted
    by city.

    :param api_key: the API key obtained from 'https://www.worldweatheronline.com/developer/'. (str)
    :param city: a city for which to retrieve data. (str)
    :param start_date: The date from which to begin data extraction, in the format 'YYYY-MM-DD'. (str)
    :param end_date: The date at which to end data extraction, in the format 'YYYY-MM-DD'. (str)
    :param frequency: the frequency of extracted data, measured in hours. (int)
    :param verbose: boolean determining printing during data extraction. (bool)
    :param csv_directory: an optional file directory to store the output. (os directory)
    :return: dataset: a Pandas DataFrame containing the requested weather data. (Pandas DataFrame)
    """

    def __init__(self,
                 api_key: str,
                 city: str,
                 start_date: str,
                 end_date: str,
                 frequency: int,
                 verbose: bool = True,
                 csv_directory: str = os.getcwd()):

        if not all(isinstance(v, str) for v in [api_key, city, start_date, end_date, csv_directory]):
            raise TypeError("The 'api_key', 'city', 'start_date', 'end_date' "
                            "and 'csv_directory' arguments must be string types.")
        if not isinstance(frequency, int):
            raise TypeError("frequency argument must be an integer object.")

        end_date_datetime = datetime.strptime(end_date, '%Y-%m-%d')
        start_date_datetime = datetime.strptime(start_date, '%Y-%m-%d')
        if start_date_datetime >= end_date_datetime:
            raise ValueError("The end_date argument cannot occur prior to the start_date argument.")
        if frequency not in [1, 3, 6, 12]:
            raise ValueError("The frequency argument (hours) must be selected from: 1, 3, 6, 12.")

        self.api_key = api_key
        self.city = city
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_datetime = start_date_datetime
        self.end_date_datetime = end_date_datetime
        self.frequency = frequency
        self.verbose = verbose
        self.csv_directory = csv_directory

    @staticmethod
    def _extract_data(dataset: pd.DataFrame):
        """
      This internal function extracts data from the output of the
      _retrieve_this_city internal function below.

      :param dataset: a json file containing extracted data. (json)
      :returns: monthly_data: a Pandas DataFrame containing the requested weather data. (Pandas DataFrame)
      """
        number_days = len(dataset)
        monthly_data = pd.DataFrame()
        for i in range(number_days):
            d = dataset[i]
            astronomy_data = pd.DataFrame(d['astronomy'])
            hourly_data = pd.DataFrame(d['hourly'])

            required_keys = ['date', 'maxtempC', 'mintempC', 'totalSnow_cm', 'sunHour', 'uvIndex']
            subset_d = dict((k, d[k]) for k in required_keys if k in d)
            weather_data = pd.DataFrame(subset_d, index=[0])
            data = pd.concat([weather_data.reset_index(drop=True), astronomy_data], axis=1)
            data = pd.concat([data, hourly_data], axis=1)
            data = data.fillna(method='ffill')

            data['time'] = data['time'].apply(lambda x: x.zfill(4))
            data['time'] = data['time'].str[:2]
            data['date_time'] = pd.to_datetime(data['date'] + ' ' + data['time'])

            columns_required = ['date_time', 'maxtempC', 'mintempC', 'totalSnow_cm', 'sunHour', 'uvIndex',
                                'moon_illumination', 'moonrise', 'moonset', 'sunrise', 'sunset',
                                'DewPointC', 'FeelsLikeC', 'HeatIndexC', 'WindChillC', 'WindGustKmph',
                                'cloudcover', 'humidity', 'precipMM', 'pressure', 'tempC', 'visibility',
                                'winddirDegree', 'windspeedKmph']

            data = data[columns_required]
            data = data.loc[:, ~data.columns.duplicated()]
            monthly_data = pd.concat([monthly_data, data])
        return monthly_data

    def _retrieve_this_city(self, city):
        """
      This internal function retrieves the data corresponding to the city
      specified within the input arguments, for the specified frequency between
      the start_date_datetime and end_date_datetime arguments.

      :param city: the city which the user wishes to extract. (string)
      :return: historical_data: a Pandas DataFrame containing the requested historical data. (Pandas DataFrame)


      """
        start_time = datetime.now()

        list_month_begin = pd.date_range(self.start_date, self.end_date, freq='MS', closed='right')
        list_month_begin = pd.concat([pd.Series(pd.to_datetime(self.start_date)), pd.Series(list_month_begin)],
                                     ignore_index=True)

        list_month_end = pd.date_range(self.start_date_datetime, self.end_date_datetime, freq='M', closed='left')
        list_month_end = pd.concat([pd.Series(list_month_end), pd.Series(pd.to_datetime(self.end_date))],
                                   ignore_index=True)

        total_months = len(list_month_begin)

        historical_data = pd.DataFrame()
        for m in range(total_months):
            start_d = str(list_month_begin[m])[:10]
            end_d = str(list_month_end[m])[:10]
            if self.verbose:
                print('Retrieving data for ' + city + ' from: ' + start_d + ' to: ' + end_d)
            url_page = 'http://api.worldweatheronline.com/premium/v1/past-weather.' \
                       'ashx?key={}&q={}&format=json&date={}&enddate={}&tp={}'.format(self.api_key,
                                                                                      city,
                                                                                      start_d,
                                                                                      end_d,
                                                                                      str(self.frequency))
            json_page = urllib.request.urlopen(url_page, timeout=10)
            json_data = json.loads(json_page.read().decode())
            data = json_data['data']['weather']

            data_this_month = self._extract_data(data)
            data_this_month['city'] = city
            historical_data = pd.concat([historical_data, data_this_month])

            time_elapsed = datetime.now() - start_time
            if self.verbose:
                print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))

        return historical_data

    def retrieve_hist_data(self):
        """
      This function calls the above internal functions, collecting the data from the
      WorldWeatherOnline API. If a csv directory is provided, a csv file shall be generated
      and stored for this city. Additionally, a dataframe 'dataset' is materialised.

      :returns: dataset: a Pandas DataFrame containing the requested historical data. (Pandas DataFrame)
      """
        if self.verbose:
            print('\n\nRetrieving weather data for ' + self.city + '\n\n')
        dataset = self._retrieve_this_city(self.city)
        dataset.set_index('date_time', drop=True, inplace=True)

        if self.csv_directory:
            dataset.to_csv(self.csv_directory + '/' + self.city + '.csv', header=True, index=True)
            if self.verbose:
                print('\n\nexport ' + self.city + ' completed!\n\n')

        return dataset
