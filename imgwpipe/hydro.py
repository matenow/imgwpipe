import os
import zipfile as zp
import pandas as pd
import numpy as np
import core
import requests


class Labels:
	init_cols = [
		'Station ID', 'Station name', 'River/Lake name', 'Hydrological year', 'Hydrological month indicator', 'Day',
		'Water level', 'Water flow', 'Water temperature', 'Month']

	trans_cols = [
		'Date', 'Year', 'Month', 'Day', 'Hydrological year', 'Hydrological month indicator', 'Station ID', 'Station name',
		'River/Lake name', 'River/Lake ID', 'Water level', 'Water flow', 'Water temperature']


def transform(trans_df):
	trans_df = trans_df.reset_index().drop('index', axis=1)
	dfc = trans_df.copy()
	lstrip = 'AĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻaąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż( '
	river_lake_id = dfc['River/Lake name'].map(lambda x: x.lstrip(lstrip).rstrip(')'))
	trans_df['River/Lake name'] = trans_df['River/Lake name'].map(lambda x: x.rstrip(' ()1234567890 '))
	trans_df['River/Lake ID'] = river_lake_id

	trans_df['Month'] = trans_df['Month'].fillna(method='ffill').astype(int)
	trans_df['Day'] = trans_df['Day'].fillna(method='ffill').astype(int)

	trans_df['Year'] = trans_df['Hydrological year']
	trans_df.loc[(trans_df['Month'] == 11) | (trans_df['Month'] == 12), 'Year'] = trans_df['Year'].astype(int) - 1
	trans_df['Date'] = pd.to_datetime(trans_df[['Year', 'Month', 'Day']])

	trans_df = trans_df[Labels.trans_cols]
	trans_df.loc[trans_df['Water level'] == 9999, 'Water level'] = np.nan
	trans_df.loc[trans_df['Water flow'] == 99999.999, 'Water flow'] = np.nan
	trans_df.loc[trans_df['Water temperature'] == 99.9, 'Water temperature'] = np.nan
	return trans_df


def getframe(year: int, month: int, station='', stationid=''):
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
	if not station == '' and not stationid == '':
		df = df.loc[(df['Station name'] == station) & (df['Station ID'] == stationid)]
	os.remove(f'temp/{zipname}')
	os.remove(f'temp/{csvname}')
	return df


def getyear(year: int, station=''):
	year_df = pd.DataFrame([], columns=Labels.init_cols)
	for month in range(1, 12+1):
		df = getframe(year, month, station)
		year_df = year_df.append(df)
	year_df = transform(year_df)
	if not station == '':
		year_df.to_csv(f'temp/hydro_daily_{year}_{station}.csv', index=False, encoding='utf-8')
	else:
		year_df.to_csv(f'temp/hydro_daily_{year}_all.csv', index=False, encoding='utf-8')
	return year_df


def getrange(first_year: int, last_year: int, station=''):
	if first_year < 1951 or last_year > 2020:
		print('Selected years out of the available range (1951-2020).')
	else:
		range_df = pd.DataFrame([], columns=Labels.trans_cols)
		for year in range(first_year, last_year + 1):
			df = getyear(year, station)
			range_df = range_df.append(df, ignore_index=True).reset_index().drop('index', axis=1)
		if not station == '':
			range_df.to_csv(f'temp/hydro_daily_range_{first_year}-{last_year}_{station}.csv', index=False, encoding='utf-8')
		else:
			range_df.to_csv(f'temp/hydro_daily_range_{first_year}-{last_year}_all.csv', index=False, encoding='utf-8')
		return range_df


def getmonth(year: int, month: int, station=''):
	month_df = getframe(year, month, station)
	month_df.columns = Labels.init_cols
	month_df = transform(month_df)
	if not station == '':
		month_df.to_csv(f'temp/hydro_daily_{year}_{core.strnumb(month)}_{station}.csv', index=False, encoding='utf-8')
	else:
		month_df.to_csv(f'temp/hydro_daily_{year}_{core.strnumb(month)}_all.csv', index=False, encoding='utf-8')
	return month_df


def month_stations(year: int, month: int, csv=False) -> list:
	return getmonth(year, month)['Station name'].sort_values().unique().tolist()


def year_stations(year: int) -> list:
	return getyear(year)['Station name'].sort_values().unique().tolist()
