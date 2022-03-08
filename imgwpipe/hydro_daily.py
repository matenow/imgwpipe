import os
import zipfile as zp
import pandas as pd
import numpy as np
import core
import requests


class Labels:
	init_cols = [
		'station_id', 'station_name', 'riv_or_lake', 'hydro_y', 'hydro_month_ind', 'day',
		'lvl', 'flow', 'temp', 'month']

	trans_cols = [
		'date', 'year', 'month', 'day', 'hydro_y', 'hydro_month_ind', 'station_id', 'station_name',
		'riv_or_lake', 'riv_or_lake_id', 'lvl', 'flow', 'temp']


def transform(trans_df):
	trans_df = trans_df.reset_index().drop('index', axis=1)
	dfc = trans_df.copy()
	lstrip = 'AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻaąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż( '
	river_lake_id = dfc['riv_or_lake'].map(lambda x: x.lstrip(lstrip).rstrip(')'))
	trans_df['riv_or_lake'] = trans_df['riv_or_lake'].map(lambda x: x.rstrip(' ()1234567890 '))
	trans_df['riv_or_lake_id'] = river_lake_id

	trans_df['month'] = trans_df['month'].fillna(method='ffill').astype(int)
	trans_df['day'] = trans_df['day'].fillna(method='ffill').astype(int)

	trans_df['year'] = trans_df['hydro_y']
	trans_df.loc[(trans_df['month'] == 11) | (trans_df['month'] == 12), 'year'] = trans_df['year'].astype(int) - 1
	trans_df['date'] = pd.to_datetime(trans_df[['year', 'month', 'day']])

	trans_df = trans_df[Labels.trans_cols]
	trans_df.loc[trans_df['lvl'] == 9999, 'lvl'] = np.nan
	trans_df.loc[trans_df['flow'] == 99999.999, 'flow'] = np.nan
	trans_df.loc[trans_df['temp'] == 99.9, 'temp'] = np.nan
	return trans_df


def getframe(year: int, month: int, stationid=None, station=None):

	core.makedir(dirname='temp')
	zipname = f'codz_{year}_{core.strnumb(month)}.zip'
	csvname = f'codz_{year}_{core.strnumb(month)}.csv'
	url = f'https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_hydrologiczne/dobowe/{year}/{zipname}'
	r = requests.get(url)
	with open(f'temp/{zipname}', 'wb') as file:
		file.write(r.content)

	with zp.ZipFile(f'temp/{zipname}', 'r') as zip_ref:
		zip_ref.extractall(path='temp')
	df = pd.read_csv(f'temp/{csvname}', encoding='windows-1250', header=None)
	df.columns = Labels.init_cols
	if stationid is not None:
		df = df.loc[df['station_id'] == int(stationid)]
	elif station is not None:
		df = df.loc[df['station_name'] == station]

	os.remove(f'temp/{zipname}')
	os.remove(f'temp/{csvname}')
	return df


def getyear(year: int, stationid=None, station=None, save=False):
	err(stationid, station)
	if not isinstance(year, int):
		raise Exception('year argument must be an integer')
	elif year not in range(1951, 2021):
		raise Exception('chosen year not in available range (1951, 2020)')
	else:
		year_df = pd.DataFrame([], columns=Labels.init_cols)
		for month in range(1, 12+1):
			df = getframe(year, month, stationid, station)
			year_df = year_df.append(df)
		year_df = transform(year_df)
		if save:
			core.makedir('Saved')
			if stationid is not None:
				year_df.to_csv(f'Saved/hydro_daily_{year}_{stationid}.csv', index=False, encoding='utf-8')
			elif station is not None:
				year_df.to_csv(f'Saved/hydro_daily_{year}_{station}.csv', index=False, encoding='utf-8')
			elif stationid is None or station is None:
				year_df.to_csv(f'Saved/hydro_daily_{year}_all.csv', index=False, encoding='utf-8')
		return year_df


def getrange(first_year: int, last_year: int, stationid=None, station=None, save=False):
	err(stationid, station)
	if not isinstance(first_year, int) or not isinstance(last_year, int):
		raise Exception('first_year and last_year arguments must be integers')
	elif first_year not in range(1951, 2021) or last_year not in range(1951, 2021):
		raise Exception('chosen year out of available range (1951-2020)')
	else:
		range_df = pd.DataFrame([], columns=Labels.trans_cols)
		for year in range(first_year, last_year + 1):
			df = getyear(year, stationid, station)
			range_df = range_df.append(df, ignore_index=True).reset_index().drop('index', axis=1)
		if save:
			core.makedir('Saved')
			if stationid is not None:
				range_df.to_csv(f'Saved/hydro_daily_range_{first_year}-{last_year}_{stationid}.csv', index=False, encoding='utf-8')
			elif station is not None:
				range_df.to_csv(f'Saved/hydro_daily_range_{first_year}-{last_year}_{station}.csv', index=False, encoding='utf-8')
			elif stationid is None or station is None:
				range_df.to_csv(f'Saved/hydro_daily_range_{first_year}-{last_year}_all.csv', index=False, encoding='utf-8')
		return range_df


def getmonth(year: int, month: int, stationid=None, station=None, save=False) -> object:
	err(stationid, station)
	if not isinstance(year, int) or not isinstance(month, int):
		raise Exception('year and month arguments must be integers')
	elif month not in range(1, 13):
		raise Exception('chosen month not in range (1-12)')
	elif year not in range(1951, 2021):
		raise Exception('chosen year not in available range (1951-2020)')
	else:
		month_df = getframe(year, month, stationid, station)
		if month_df.empty:
			raise Exception('there is no station with chosen name or id')
		else:
			month_df.columns = Labels.init_cols
			month_df = transform(month_df)
		if save:
			core.makedir('Saved')
			if stationid is not None:
				month_df.to_csv(f'Saved/hydro_daily_{year}_{core.strnumb(month)}_{stationid}.csv', index=False, encoding='utf-8')
			elif station is not None:
				month_df.to_csv(f'Saved/hydro_daily_{year}_{core.strnumb(month)}_{station}.csv', index=False, encoding='utf-8')
			elif stationid is None or station is None:
				month_df.to_csv(f'Saved/hydro_daily_{year}_{core.strnumb(month)}_all.csv', index=False, encoding='utf-8')
		return month_df


def stations(year: int, month=None) -> list:
	if not isinstance(year, int):
		raise Exception('year argument must be an integer')
	elif month is not None:
		stations_names = getmonth(year, month)['station_name'].sort_values()
		stations_ids = getmonth(year, month)['station_id'].sort_values()
	else:
		stations_names = getyear(year)['station_name'].sort_values()
		stations_ids = getyear(year)['station_id'].sort_values()
	stations_list = list()
	for x, y in zip(stations_names, stations_ids):
		stations_list.append(f'{y}, {x}')
	return list(set(stations_list))


def err(stationid, station):
	if not isinstance(stationid, str) and stationid is not None:
		raise Exception('stationid argument must be a string value')
	elif not isinstance(station, str) and station is not None:
		raise Exception('station argument must be a string value')

