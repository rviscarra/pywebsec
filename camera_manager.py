#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       camera_manager.py
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

from optparse import OptionParser
from configuration import Configuration
from glob import glob
from opencv import highgui
import opencv as cv
import re

class Camera:

	def __init__(self, device_path, haarfiles):
		
		self.haarfiles = haarfiles
		self.device_path = device_path
		self.id = self._get_device_id()
	
	def init(self):
		self.device = highgui.cvCreateCameraCapture(self.id)
	
		
	def get_device_path(self):
		
		return self.device_path
	
	
	def _get_device_id(self):
		
		res = re.findall(r'.*?(\d+)', self.device_path)
		return int(res[0]) if len(res) > 0 else 0
		
	
	def get_frame(self, face_rec = False):
		
		image = highgui.cvQueryFrame(self.device)
		
		if face_rec:
			
			grayscale = cv.cvCreateImage(cv.cvSize(640, 480), 8, 1)
			cv.cvCvtColor(image, grayscale, cv.CV_BGR2GRAY)
			storage = cv.cvCreateMemStorage(0)
			cv.cvClearMemStorage(storage)
			cv.cvEqualizeHist(grayscale, grayscale)
			
			for cascade in self.haarfiles:
				matches = cv.cvHaarDetectObjects(grayscale, cascade, storage, 1.2, 2, 
										  cv.CV_HAAR_DO_CANNY_PRUNING, cv.cvSize(100,100))
			  
				if matches:
					for i in matches:
						cv.cvRectangle(image, cv.cvPoint( int(i.x), int(i.y)),
							cv.cvPoint(int(i.x+i.width), int(i.y+i.height)),
							cv.CV_RGB(0,0,255), 2, 5, 0)
			
			image = cv.cvGetMat(image)
			
		return image
	
	def save_frame(self, image_path):
		
		highgui.cvSaveImage(image_path, self.get_frame())
			
	
class CameraManager:
	
	def __init__(self):
		conf = Configuration.get()
		hdir = conf['haar_classifiers_dir']
		
		self.haarfiles = [ cv.cvLoadHaarClassifierCascade(str(hdir + h), cv.cvSize(10, 10)) for h in conf['haar_classifiers'] ]

		self.camera_devices = glob(conf['cameras_glob'])
	
	def get_cameras(self):
		return [ Camera(camera, self.haarfiles) for camera in self.camera_devices ]
	
	def get_camera(self, device):
		return Camera(device, self.haarfiles)
		
	def get_camera_by_id(self, id):
		
		cameras = self.get_cameras()
		camera = filter(lambda c: c.id == id, cameras)
		
		return camera[0] if len(camera) > 0 else None
	
	

if __name__ == '__main__':
	
	# Opciones de la linea de comandos
	parser = OptionParser()
	
	parser.add_option('-d', '--device', dest='device', default=None, help='Ruta de dispositivo correspondiente a una camara web')
	
	parser.add_option('-f', '--face', dest='face', default=False, action='store_true', help='Indica si se detectaran imagenes en la camara')

	options = parser.parse_args()[0]
	
	if options.device:
		
		manager = CameraManager()
		
		camera = manager.get_camera(options.device)
		
		camera.init()
			
		keep_running = True
		
		def mouse_callback(event, x, y, flags, params):
			global keep_running
			if event == highgui.CV_EVENT_LBUTTONDOWN:
				keep_running = False
					
		wname = 'Monitor de Camara[ {0} ]'.format(options.device)

		highgui.cvNamedWindow(wname, 1)
		highgui.cvSetMouseCallback(wname, mouse_callback, ())
		
		while keep_running:
		
			img = camera.get_frame(options.face)
			
			highgui.cvShowImage(wname, img)
			key = highgui.cvWaitKey(10)
			if key > 0:
				
				break
				
				
		
