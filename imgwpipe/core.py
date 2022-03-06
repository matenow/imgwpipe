import os
import shutil
import pandas as pd


def makedir(dirname: str):
	if not os.path.exists(dirname):
		os.makedirs(dirname)


def clear(dirname: str):
	if os.path.exists(dirname):
		shutil.rmtree(path=dirname)


def strnumb(number: int):
	if number < 10:
		str_num = f'0{number}'
	else:
		str_num = f'{number}'
	return str_num


def fixdate(df):
	df['Date'] = pd.to_datetime(df['Date'])
	return df
