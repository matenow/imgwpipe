import os
import zipfile as zp
import pandas as pd
import numpy as np
import core
import requests


class Labels:
	init_cols = [
		'station_id', 'station_name', 'riv_or_lake', 'hydroy', 'hydrom', 'day',
		'lvl', 'flow', 'temp', 'month']

	trans_cols = [
		'date', 'year', 'month', 'day', 'hydroy', 'hydrom', 'station_id', 'station_name',
		'riv_or_lake', 'riv_or_lake_id', 'lvl', 'flow', 'temp']


def transform(trans_df):
	trans_df = trans_df.reset_index().drop('index', axis=1)
	dfc = trans_df.copy()
	lstrip = 'AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻaąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż( '
	rivlakeid = dfc['riv_or_lake'].map(lambda x: x.lstrip(lstrip).rstrip(')'))
	trans_df['riv_or_lake'] = trans_df['riv_or_lake'].map(lambda x: x.rstrip(' ()1234567890 '))
	trans_df['riv_or_lake_id'] = rivlakeid

	trans_df['month'] = trans_df['month'].fillna(method='ffill').astype(int)
	trans_df['day'] = trans_df['day'].fillna(method='ffill').astype(int)

	trans_df['year'] = trans_df['hydroy']
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
		raise Exception('year argument not in available range (1951, 2020)')
	else:
		year_df = pd.DataFrame([], columns=Labels.init_cols)
		for month in range(1, 12+1):
			df = getframe(year, month, stationid, station)
			year_df = pd.concat([year_df, df], ignore_index=True)
		year_df = transform(year_df)
		if save:
			core.makedir('Saved')
			if stationid is not None:
				year_df.to_csv(f'Saved/hydro_daily_{year}_{stationid}.csv', index=False, encoding='utf-8')
			elif station is not None:
				year_df.to_csv(f'Saved/hydro_daily_{year}_{station}.csv', index=False, encoding='utf-8')
			elif stationid is None or station is None:
				year_df.to_csv(f'Saved/hydro_daily_{year}_all.csv', index=False, encoding='utf-8')
		return year_df.reset_index().drop('index', axis=1)


def getrange(first_year: int, last_year: int, stationid=None, station=None, save=False):
	err(stationid, station)
	if not isinstance(first_year, int) or not isinstance(last_year, int):
		raise Exception('first_year and last_year arguments must be integers')
	elif first_year not in range(1951, 2021) or last_year not in range(1951, 2021):
		raise Exception('year argument out of available range (1951-2020)')
	else:
		range_df = pd.DataFrame([], columns=Labels.trans_cols)
		for year in range(first_year, last_year + 1):
			for month in range(1, 12+1):
				df = getframe(year, month, stationid, station)
				range_df = pd.concat([range_df, df], ignore_index=True)
		range_df = transform(range_df)
		if save:
			core.makedir('Saved')
			if stationid is not None:
				range_df.to_csv(f'Saved/hydro_daily_range_{first_year}-{last_year}_{stationid}.csv', index=False, encoding='utf-8')
			elif station is not None:
				range_df.to_csv(f'Saved/hydro_daily_range_{first_year}-{last_year}_{station}.csv', index=False, encoding='utf-8')
			elif stationid is None or station is None:
				range_df.to_csv(f'Saved/hydro_daily_range_{first_year}-{last_year}_all.csv', index=False, encoding='utf-8')
		return range_df.reset_index().drop('index', axis=1)


def getmonth(year: int, month: int, stationid=None, station=None, save=False):
	err(stationid, station)
	if not isinstance(year, int) or not isinstance(month, int):
		raise Exception('year and month arguments must be integers')
	elif month not in range(1, 13):
		raise Exception('month argument not in range (1-12)')
	elif year not in range(1951, 2021):
		raise Exception('year argument not in available range (1951-2020)')
	else:
		month_df = getframe(year, month, stationid, station)
		if month_df.empty:
			raise Exception('there is no station with chosen name or id ')
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


def err(stationid, station):
	if not isinstance(stationid, int) and stationid is not None:
		raise Exception('stationid argument must be an integer')
	elif not isinstance(station, str) and station is not None:
		raise Exception('station argument must be a string')


def metadata(stationid: int, data: str) -> list:
	if stationid is None:
		raise Exception('missing stationid argument')
	elif not isinstance(stationid, int) and stationid is not None:
		raise Exception('stationid argument must be an integer')

	meta = pd.read_csv('metadata/hydro_stations.csv', encoding='utf-8')

	if meta.loc[meta['id'] == stationid].empty:
		raise Exception('station with chosen id does not exist')

	if data == 'coords':
		xcoord = meta.loc[meta['id'] == stationid]['X'].unique()[0]
		ycoord = meta.loc[meta['id'] == stationid]['Y'].unique()[0]
		return [xcoord, ycoord]
	elif data == 'riv_or_lake':
		rivlake = meta.loc[meta['id'] == stationid]['riv_or_lake'].unique()[0]
		rivlakeid = meta.loc[meta['id'] == stationid]['riv_or_lake_id'].unique()[0]
		return [rivlake, rivlakeid]
	elif data == 'station_name':
		station_name = meta.loc[meta['id'] == stationid]['name'].unique()[0]
		return [station_name]
	else:
		raise Exception('unknown data argument')


def stations(year: int, month=None) -> list:
	if not isinstance(year, int):
		raise Exception('year argument must be an integer')
	elif not isinstance(month, int) and month is not None:
		raise Exception('month argument must be an integer')
	elif month not in range(1, 13) and month is not None:
		raise Exception('month argument not in range (1-12)')
	elif month is not None:
		stations_names = getmonth(year, month)['station_name'].sort_values()
		stations_ids = getmonth(year, month)['station_id'].sort_values()
	else:
		stations_names = getyear(year)['station_name'].sort_values()
		stations_ids = getyear(year)['station_id'].sort_values()
	stations_list = list()
	for x, y in zip(stations_names, stations_ids):
		stations_list.append(y)
	return list(set(stations_list))

