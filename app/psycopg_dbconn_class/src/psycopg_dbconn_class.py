#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Kleydson Stenio <kleydson.stenio@gmail.com>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

# Imports
try:
	import psycopg2
except ImportError as ie:
	print(
		'Please install psycopg2-binary library in order to use this class.\n'
		'Check: https://pypi.org/project/psycopg2-binary/')
	raise ie
else:
	import os
	import json
	import psycopg2.extras
	from pathlib import Path


# Main Class
class DataBaseConnection(object):
	__default_keys = ('DBN', 'DBU', 'DBK', 'DBH', 'DBP')
	__default_cursor = ''
	
	def __init__(
			self, config_file: Path = None, auto_config: bool = True, auto_config_mode: str = 'env',
			auto_connect: bool = False, default_cursor: str = ''):
		"""
		DataBaseConnection constructor
		:param config_file: location (pathlib) of JSON config file
		:param auto_config: if the config parameters will be loaded on object creation
		:param auto_config_mode: mode for auto config, 'env' or 'json'
		:param auto_connect: if class will try to connect on creation
		:param default_cursor: default cursor for queries return, 'realdict' (default) or 'dict'
		"""
		# Checks errors
		if not isinstance(default_cursor, str):
			raise ValueError(
				f'Invalid type for cursor_type parameter. '
				f'Expected *str*, found **{default_cursor.__class__.__name__}**.')
		if default_cursor.lower() not in ('', 'realdict', 'dict'):
			raise ValueError('Invalid value for cursor_type parameter. Accepted values are "realdict" and "dict".')
		self.__config = {'db_name': '', 'db_host': '', 'db_port': '', 'db_user': '', 'db_pass': ''}
		self.__default_cursor = default_cursor
		self.cursor = None
		self.connection = None
		self.connected = False
		if auto_config:
			if auto_config_mode == 'env':
				self.update_config_values_from_env()
			elif auto_config_mode == 'json':
				self.update_config_values_from_json(config_file)
			if auto_connect:
				self.connect()
	
	def update_config_values(self, name: str, host: str, port: str, user: str, password: str):
		"""
		Method for handling change of connection/config values
		:param name: name of database
		:param host: ip/host of database
		:param port: database port
		:param user: database user
		:param password: database password
		:return:
		"""
		self.__config['db_name'] = name
		self.__config['db_host'] = host
		self.__config['db_port'] = port
		self.__config['db_user'] = user
		self.__config['db_pass'] = password
	
	def update_config_value(self, key: str, value: str):
		"""
		Method for updating a single config value of object
		:param key: the key to update
		:param value: the value of the key
		:return:
		"""
		self.__config[key] = value
	
	def update_config_values_from_json(self, config_file: Path = None):
		"""
		Method for updating config values from JSON
		:param config_file: the JSON file Path
		:return:
		"""
		# Checks if user entered config_file parameter
		if config_file is None:
			candidate_file = Path(__file__).parent.joinpath('conn.json')
		else:
			candidate_file = config_file
		# Now, checks if candidate_file exists
		if candidate_file.is_file():
			with candidate_file.open('r+') as js:
				loaded_config = json.load(js)
			# With json file loaded, we must guarantee that the correct fields exists
			keys = ('db_name', 'db_host', 'db_port', 'db_user', 'db_pass')
			if all([key in keys for key in loaded_config]):
				self.__config['db_name'] = loaded_config['db_name']
				self.__config['db_host'] = loaded_config['db_host']
				self.__config['db_port'] = loaded_config['db_port']
				self.__config['db_user'] = loaded_config['db_user']
				self.__config['db_pass'] = loaded_config['db_pass']
			else:
				raise ValueError(
					f'The json file ({candidate_file.name}) does not have the '
					f'needed/correct fields to connect into the DB .\n'
					f'Needed values: {str(keys)}')
		else:
			raise FileNotFoundError(
				f'Could not find the _{candidate_file.absolute()}_ file')
	
	def update_config_values_from_env(self, env_keys: tuple = None):
		"""
		Method for updating config values from environment variables
		:param env_keys: the keys being used in environment. Tuple is loaded in order:
			db_name, db_user, db_pass, db_host, db_port (0, 1, 2, 3, 4)
		:return:
		"""
		# Checks env keys
		if env_keys is None:
			env_keys = self.__default_keys
		elif len(env_keys) != 5:
			raise AssertionError('Illegal size for env_keys! (!= 5)')
		self.__config['db_name'] = os.environ.get(env_keys[0])
		self.__config['db_user'] = os.environ.get(env_keys[1])
		self.__config['db_pass'] = os.environ.get(env_keys[2])
		self.__config['db_host'] = os.environ.get(env_keys[3])
		self.__config['db_port'] = os.environ.get(env_keys[4])
	
	def connect(self, cursor_type: str = 'realdict'):
		"""
		Simple method for database connection (object must have proper config before connecting)
		:param cursor_type: type of cursor, being 'realdict' or 'dict'
		:return:
		"""
		if not self.connected:
			# Check if all parameters were set before connecting
			if all([self.__config[x] != '' for x in self.__config]):
				# All fine
				cursor_type = self.__default_cursor if self.__default_cursor else cursor_type
				cfactory = psycopg2.extras.RealDictCursor if cursor_type == 'realdict' else psycopg2.extras.DictCursor
				try:
					connection = psycopg2.connect(
						dbname=self.__config['db_name'],
						host=self.__config['db_host'],
						port=self.__config['db_port'],
						user=self.__config['db_user'],
						password=self.__config['db_pass'],
						cursor_factory=cfactory)
				except psycopg2.OperationalError as err:
					print(
						f'Could not connect to the database _{self.__config["db_name"]}_')
					raise err
				else:
					connection.cursor().execute("SET client_connection_check_interval TO 2000")
					connection.commit()
					self.connection = connection
					self.cursor = connection.cursor()
					self.connected = True
					print(
						f'Successfully connected to the Postgres Database '
						f'_{self.__config["db_name"]}_ on '
						f'{self.__config["db_host"]}:{self.__config["db_port"]}')
			else:
				raise ValueError(
					'Please, setup connection parameters before trying to connect to a server! '
					'Tip: run the methods update_config_values or update_config_values_from_json')
	
	def run_query(self, query: str, values: list = None, force: bool = True, do_print: bool = False):
		"""
		Method for running queries on connected database. Obs.: This does not return values
		:param query: the query itself
		:param values: values to pass to query
		:param force: will attempt to force database connection
		:param do_print: will print returned messages (if there are any)
		:return:
		"""
		if force:
			if not self.connected:
				self.connect()
		if self.connected:
			try:
				if values is None:
					self.cursor.execute(query)
				else:
					self.cursor.execute(query, values)
					# TODO: investigate more on psycopg2.sql.SQL and try to update this command with it
			except psycopg2.OperationalError as err:
				print(f'Could not execute query _{query}_')
				raise err
			else:
				self.connection.commit()
				if do_print:
					print(
						f'Query **{query}** executed in _{self.__config["db_name"]}_')
		else:
			raise ConnectionError('There is no Database connected')
	
	def run_read_query(self, query: str, values: list = None, force: bool = True, fetch_all: bool = False):
		"""
		Similar to run_query, but returns values obtained from database
		:param query: the query itself
		:param values: values to pass to query
		:param force: will attempt to force database connection
		:param fetch_all: catches all rows (or just a single one)
		:return:
		"""
		if force:
			if not self.connected:
				self.connect()
		if self.connected:
			try:
				if values is None:
					self.cursor.execute(query)
				else:
					if type(values) is list:
						self.cursor.execute(query, values)
					else:
						raise TypeError(f'Values must be a list, not {type(values).__name__}')
			except psycopg2.OperationalError as err:
				print(f'Could not execute query **{query}** with values **{values}**')
				raise err
			except psycopg2.errors.InFailedSqlTransaction:
				self.connection.rollback()
				self.cursor.execute(query, values)
				result = self.cursor.fetchall() if fetch_all else self.cursor.fetchone()
				self.connection.commit()
				return result
			except Exception as ex:
				raise ex
			else:
				result = self.cursor.fetchall() if fetch_all else self.cursor.fetchone()
				self.connection.commit()
				return result
		raise ConnectionError('There is no Database connected')
	
	def close(self):
		"""
		Simple method for closing the database connection
		:return:
		"""
		if self.connected:
			self.connection.close()
			self.connected = False
			print(f'Closed connection to _{self.__config["db_name"]}_')
