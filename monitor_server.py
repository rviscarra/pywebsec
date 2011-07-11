#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       monitor_server.py
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

import cgi
from optparse import OptionParser
from Cheetah.Template import Template
from camera_manager import CameraManager
import BaseHTTPServer as http
from configuration import Configuration

current_camera = None

mcm = CameraManager()

class RemoteCameraRequestHandler(http.BaseHTTPRequestHandler):
	
	def do_GET(self):
		if self.path == '/':
			path = self.path
			action = 'index'
		else:
			path = self.path.split('/')
			action = path[1]
		
		self._handle_action(action, *path[2:] if len(path) > 2 else [] )
		
	
	def _handle_action(self, action, *args):	
		
		if action == 'index':
			
			self._index()
		
		elif action == 'view':
			self._view_camera(int(args[0]))
		
		elif action == 'image':
			
			self._snapshot(int(args[0]))
		
		elif action == 'cameras':
			
			if self.usuario_valido:
				
				self._list_cameras()
				
			else:
				
				self._index()
		
		elif action == 'login':
			
			pass
		
		else:
			self.send_error(404, 'No se encontro la accion [{0}]'.format(action))
	
	
	def do_POST(self):
		
		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		if ctype == 'multipart/form-data':
			query=cgi.parse_multipart(self.rfile, pdict)
		user = query.get('user')
		password = query.get('password')
		
		conf = Configuration.get()
		self.usuario_valido = (user[0] == conf['user'] and password[0] == conf['password'])
		# print user[0], conf['user'], password[0], conf['password']
		
		
		if self.usuario_valido:
			
			cm = CameraManager()
			self._render_view('cameras', cameras = cm.get_cameras())
			
		else:
			
			self._render_view('auth_form')
		
	
	def _index(self):

		self._render_view('auth_form')
		
	def _view_camera(self, camera_id):
		
		cm = CameraManager()
		
		camera = cm.get_camera_by_id(camera_id)
		
		self._render_view('view', camera = camera)
		
	def _snapshot(self, camera_id):
		
		global current_camera, mcm
		
		if current_camera == None or current_camera.id != camera_id:
		
			camera = mcm.get_camera_by_id(camera_id)
		
			camera.init()
			
			current_camera = camera
		
		image_path = 'temp/image.jpg'
		
		current_camera.save_frame(image_path)
		
		with open(image_path) as f:
			
			image = f.read()
		
		self._respond(image, 'image/jpeg')
		
		
	def _respond(self, data, content_type = 'text/html'):
		try:
			
			self.send_response(200)
			self.send_header('Content-Type', content_type)
			self.end_headers()
			self.wfile.write(data)
		except IOError as e:
			self.send_error(500, str(e))
			
	def _render_view(self, view_name, **args):
		
		inner_view = self._get_template(view_name, **args)
		main_view = self._get_template('layout', **{ 'yield': inner_view })
		
		self._respond(main_view)
		
	
	def _get_template(self, template_name = 'index', **args):
		
		template_file = './templates/{0}.tpl'.format(template_name)
		
		with open(template_file) as file:
			
			content = file.read()
		
		return Template(content, searchList = args)
		
		
	

		
		
if __name__ == "__main__":
	
	config = Configuration()
	
	parser = OptionParser()
	
	parser.add_option('-p', '--port', dest='port', default=config['listen_port'], help='Puerto en el que escuchara el servidor')
	
	options = parser.parse_args()[0]
	
	try:
		port = int(options.port)
	except ex:
		print 'Pueto erroneo [{0}]'.format(options.port)
		exit()
	
	listen_params = ('', port)
	httpd = http.HTTPServer(listen_params, RemoteCameraRequestHandler)
	httpd.serve_forever()
	
