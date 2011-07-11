#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       database_helper.py
#       
#       Copyright 2011 Rafael Viscarra <rafael@rafael-desktop>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import sqlite3 as dbapi
import os

class DatabaseHelper:
	
	_DATABASE_NAME = 'data/database.db'
	_connection = None
	
	def __init__(self):
		
		if os.path.exists(self._DATABASE_NAME):

			self.connection = dbapi.connect(self._DATABASE_NAME)
			create_database()

		else:

			self.connection = dbapi.connect(self._DATABASE_NAME)

	
	def create_database(self):
		
		for table in _tables:

			self.connection.execute(table)

	@staticmethod
	def get_connection():
		
		
	
	_tables = [ 
		""" create table conf_property (
				pkey text primary key,
				pvalues text not null
			) """,
		""" create table hour_range (
				range_id integer primary key autoincrement,
				start_hour integer not null,
				end_hour integer not null
			) """,
		""" create table activity (
				activity_id integer primary key autoincrement,
				activity_date date not null,
				description text not null
			) """]
	
