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
import time


class DatabaseHelper:
	
	_DATABASE_NAME = 'database.db'
	_TIME_DIFF = 15
	
	
	def __init__(self):
		
		if not os.path.exists(self._DATABASE_NAME):

			self.connection = dbapi.connect(self._DATABASE_NAME)
			self._create_database()

		else:

			self.connection = dbapi.connect(self._DATABASE_NAME)
		self.last = 0
	
	def _create_database(self):
		
		cursor = self.connection.cursor()
		for table in self._tables:
			
			cursor.execute(table)
		
		self.connection.commit()
		cursor.close()
	
	def insert_activity(self, activity):
		
		now = int(time.mktime(time.gmtime()))
		if (now - self.last) > self._TIME_DIFF:
			
			cursor = self.connection.cursor()
			cursor.execute('INSERT INTO activity VALUES(0, ?, ?)', (now, activity))
		
			self.connection.commit()
			cursor.close()
			self.last = now
	
	def get_activities(self):
		
		cursor = self.connection.cursor()
		
		cursor.execute('SELECT * FROM activity')
		
		return [ row for row in cursor ]
	
	def close(self):
		
		self.connection.close()
		
	_tables = [ 
		""" create table hour_range (
				range_id integer primary key autoincrement,
				start_hour integer not null,
				end_hour integer not null
			) """,
		""" create table activity (
				activity_id integer primary key autoincrement,
				activity_date integer not null,
				description text not null
			) """]
	
	
