# WorldWeatherPy

A Python library for the retrieval of historical weather data.

This library scrapes [WorldWeatherOnline.com][website] to collect historical weather data, returning a Pandas DataFrame. 
The DetermineListOfAttributes class returns all weather attributes available for retrieval through the [WorldWeatherOnline.com][website] API, whilst the HistoricalLocationWeather class retrieves an array of typically required weather attributes. The RetrieveByAttribute class can be used to request specific weather attributes, or a list of specific weather attributes, as available through the DetermineListOfAttributes class.

## Installation

From Python:
```python
pip install WorldWeatherPy
from WorldWeatherPy import DetermineListOfAttributes
from WorldWeatherPy import HistoricalLocationWeather
from WorldWeatherPy import RetrieveByAttribute
```

## Usage


#### If you are unsure of the available weather attributes:

```python
pip install WorldWeatherPy
from WorldWeatherPy import DetermineListOfAttributes
attributes = DetermineListOfAttributes(api_key, True).retrieve_list_of_options()
```
Returns a list containing all available weather attributes. If 'verbose' is set to True, this will be printed within the function call.

#### If you would like to retrieve standard weather attributes:

```python
pip install WorldWeatherPy
from WorldWeatherPy import HistoricalLocationWeather
dataset = HistoricalLocationWeather(api_key, city, start_date, end_date, frequency).retrieve_hist_data()
```
Returns a Pandas DataFrame 'dataset', which contains an array of weather attributes for the given city, between the start and end dates specified, with hourly frequency, indexed by date and time.

#### If you would like to retrieve specific weather attributes:

```python
pip install WorldWeatherPy
from WorldWeatherPy import RetrieveByAttribute
dataset = RetrieveByAttribute(api_key, attribute_list, city, start_date, end_date, frequency).retrieve_hist_data()
```
Returns a Pandas DataFrame 'dataset', which contains a list of pre-specified weather attributes for the given city, between the start and end dates specified, with hourly frequency, indexed by date and time.


## Input Arguments

| Argument | Description |
| ------ | --------- |
| api_key | the API key obtained from [https://www.worldweatheronline.com/developer/][API KEY]. (str) |
| attribute_list | a list of weather attributes to collect. (list) |
| city | a city for which to retrieve data. (str).  |
| start_date | a string in the format YYYY-MM-DD (str). |
| end_date | a string in the format YYYY-MM-DD (str). |
| frequency | the frequency of extracted data, measured in hours. (int) |
| verbose | boolean determining printing during data extraction. (bool) [Default = True] |
| csv_directory | an optional file directory to store the output. (os directory) [Default = None] |


[website]: <https://www.worldweatheronline.com/>
[API KEY]: <https://www.worldweatheronline.com/developer/>
