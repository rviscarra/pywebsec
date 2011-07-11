#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       configuration.py
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

import json

class Configuration:
	
	_DEFAULT_CONFIG_FILE = 'config.json'
	_current = None
	
	def __init__(self):
		self._config_values = None
		self._load()
	
	def _load(self):
		
		with open(Configuration._DEFAULT_CONFIG_FILE) as file:
		
			self._config_values = json.load(file)
		
		return self._config_values
	
	def get_value(self, property_name = None):
		
		return self._config_values[property_name] if property_name else self._config_values
	
	@staticmethod
	def get():
		
		conf = Configuration._current if Configuration._current else Configuration()
		Configuration._current = conf		
		return conf
	
	def __getitem__(self, key):
		return self._config_values.get(key, '')

if __name__ == '__main__':
	
	conf = Configuration.get()
	
	print conf['listen_port']
