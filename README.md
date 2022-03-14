# imgwpipe - The IMGW-PIB Data Pipeline
The main taks of the **imgwpipe** package is to provide an easy-to-use tool in Python programming language for automatic downloading, processing, visualising and saving data provided by Polish Institute of Meteorology and Water Management - National Research Institute (IMGW-PIB). 

The original datasets, publicly available as series of .csv files, are often difficult and time-consuming to clean, process and prepare toward data analysis. The purpose of this package is to simplify this process by reducing numerous queries and data filtering operations in Python to few simple and convinient functions.

# Table of Contents
1. [Instalation](#Installation)
2. [Dependencies](#Dependencies)
3. [Quick overview](#Quick_overview)
4. [Detailed description](#Detailed_description)
5. [Example of use](#Example_of_use)
6. [Acknowledgement](#Acknowledgement)

# Installation <a name="Installation"></a>
To use the code, simply clone this repo. In the future, the package will be available in PyPi repository.

# Dependencies <a name="Dependencies"></a>
List of currently required Python packages and libraries for running this package:

- [Requests - allows to download data directly from IMGW-PIB database.](https://docs.python-requests.org/en/latest/)
- [Pandas - allows to read, transform and store tables with data in a convinient way ](https://pandas.pydata.org)
- [NumPy - used for some of minor operation for cleaning numerical data.](https://numpy.org)


# Quick overview <a name="Quick_overview"></a>
## Hydrological data
### ```hydro_daily```

```getmonth()``` - downloads daily hydrological data for a range of one month into the Pandas DataFrame.

```getyear()``` - downloads daily hydrological data for a range of one year into the Pandas DataFrame.

```getrange()``` - downloads daily hydrological data for specified range given in years into the Pandas DataFrame.

```stations()``` - returns a list of stations and their ID's.

```metadata()``` - depending on input parameters, returns stations built-in metadata, like geographic coordinates, station name or river/lake name the station is located on.

# Detailed description <a name="Detailed_description"></a>
## Hydrological data
### ```hydro_daily```
### ```getmonth(year, month, stationid=None, station=None, save=False)``` 
Downloads daily hydrological data from danepubliczne.imgw.pl for a range of one month, and transforms it and returns as pandas DataFrame.
#### Parameters: 
- **year : int**

Hydrological year between 1951 and 2020. 
*Note: The hydrological year begins on November 1st and it adopts the number of the next calendar year.* 

- **month : int**

Hydrological month indicator. 
*Note: The first month in hydrological calendar is November.*

- **stationid : int, optional**

ID of the station of interest. If empty - takes all of the stations available for selected time range.

- **station : str, optional**

Name of the station of interest. It is highly recommended to use **stationid** parameter instead, due to the existence of stations with the same names but on different rivers or lakes. If **stationid** parameter is intruduced simultaneously with **station** parameter, the function will take only **stationid** value.

- **save : bool, default False**

If True, saves the DataFrame as a .csv file in ```/Saved``` directory.

### ```getyear(year, stationid=None, station=None, save=False)``` 
Downloads daily hydrological data from danepubliczne.imgw.pl for a range of one year, and transforms it and returns as pandas DataFrame.
#### Parameters: 
- **year : int**

Hydrological year between 1951 and 2020. 
*Note: The hydrological year begins on November 1st and it adopts the number of the next calendar year.*

- **stationid : int, optional**

ID of the station of interest. If empty - takes all of the stations available for selected time range.

- **station : str, optional**

Name of the station of interest. It is highly recommended to use **stationid** parameter instead, due to the existence of stations with the same names but on different rivers or lakes. If **stationid** parameter is intruduced simultaneously with **station** parameter, the function will take only **stationid** value.

- **save : bool, default False**

If True, saves the DataFrame as a .csv file in ```/Saved``` directory.

### ```getrange(first_year, last_year, stationid=None, station=None, save=False)``` 
Downloads daily hydrological data from danepubliczne.imgw.pl for a range of one year, and transforms it and returns as pandas DataFrame.
#### Parameters: 
- **first_year : int**

First hydrological year between 1951 and 2020 for the desired range of years.
*Note: The hydrological year begins on November 1st and it adopts the number of the next calendar year.* 

- **last_year : int**

First hydrological year between 1951 and 2020 for the desired range of years.
*Note: The hydrological year begins on November 1st and it adopts the number of the next calendar year.* 

- **stationid : int, optional**

ID of the station of interest. If empty - takes all of the stations available for selected time range.

- **station : str, optional**

Name of the station of interest. It is highly recommended to use **stationid** parameter instead, due to the existence of stations with the same names but on different rivers or lakes. If **stationid** parameter is intruduced simultaneously with **station** parameter, the function will take only **stationid** value.

- **save : bool, default False**
If True, saves the DataFrame as a .csv file in ```/Saved``` directory.

### ```stations(year, month=None)```
Returns a list of stations names and their ID's for a given hydrological year or a specific month.
#### Parameters 
- **year : int**

Hydrological year between 1951 and 2020. 
*Note: The hydrological year begins on November 1st and it adopts the number of the next calendar year.*

- **month : int, optional**

Hydrological month indicator.
*Note: The first month in hydrological calendar is November.*

### ```metadata(stationid, data)```
Returns built-in station metadata, like geographic coordinates, name of the station for a given ID and name of the river/lake on which station is located.
#### Parameters
- **stationid : int**

ID of the station.

- **data : str**

One of three currently available types of metadata:

```coords``` - geographic coordinates of the station in EPSG:2180 coordinate system

```riv_or_lake``` - name and ID of the river or lake on which station is located

```station_name``` - name of the station 
# Example of use <a name="Example_of_use"></a>
A simple usage example of the package is presented in [jupyter notebook](https://github.com/matenow/imgwpipe/blob/main/imgwpipe/EXAMPLE_OF_USE.ipynb)
# Acknowledgement <a name="Acknowledgement"></a>
Polish Institute of Meteorology and Water Management - National Research Institute [(IMGW-PIB)](https://www.imgw.pl) is the source of the data. For the purpose of running the script, data of the Institute of Meteorology and Water Management - National Research Institute have been processed.

Źródłem pochodzenia danych jest Instytut Meteorologii i Gospodarki Wodnej – Państwowy Instytut Badawczy [(IMGW-PIB)](https://www.imgw.pl). Na potrzeby funkcjonowania skryptu, dane Instytutu Meteorologii i Gospodarki Wodnej – Państwowego Instytutu Badawczego zostały przetworzone.
