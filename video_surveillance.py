#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       video_surveillance.py
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

import gtk
from configuration import Configuration 
import glob
import os
from camera_manager import CameraManager
from multiprocessing import Process

class MainWindow:
	
	controls = [
		'win_main', 'btn_config_events', 'btn_recognize_face', 
		'cmb_cameras', 'btn_view_camera', 'txt_port', 
		'btn_start_server', 'lst_cameras'
	]
	
	def __init__(self, config):
		
		self.config = config
		
		self.cm = CameraManager()
		self.builder = gtk.Builder()
		self.builder.add_from_file('win_main.xml')
		
		self._init_controls()
		self._connect_events()
		
	def _init_controls(self):
		
		for c in self.controls:
			self.__dict__[c] = self.builder.get_object(c)
			
		cell = gtk.CellRendererText()
		self.cmb_cameras.pack_start(cell, True)
		self.cmb_cameras.add_attribute(cell, "text", 0)
		self._fill_cameras()
		
	def _fill_cameras(self):
		self.cmb_cameras.get_model().clear()
		for cam in self.cm.get_cameras():
			self.cmb_cameras.append_text(cam.device_path)
			
		self.cmb_cameras.set_active(0)

	def _connect_events(self):
		self.win_main.connect('delete_event', self._win_main_delete_event)
		self.btn_view_camera.connect('clicked', self._view_camera)
		self.btn_start_server.connect('clicked', self._start_server)
		
	def _start_server(self, *args):
		puerto = self.txt_port.get_text()
		print 'Servidor iniciado en puerto', puerto
		
	def _win_main_delete_event(self, *args):
		gtk.main_quit()
		
	
	def _view_camera(self, *args):
		
		device = self.cmb_cameras.get_active_text()
		
		proc = Process(target = MainWindow._start_camera_monitor, 
			args = (device,) )
			
		proc.start()
	
	@staticmethod
	def _start_camera_monitor(device):
		
		os.popen(' '.join(('python', 'camera_manager.py', '-d', device, '-f')))
		
	
	def main(self):
		self.win_main.show_all()
		gtk.main()

if __name__ == "__main__":
	
	config = Configuration.get()
	mainWin = MainWindow(config)
	mainWin.main()
