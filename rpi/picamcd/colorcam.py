import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
from colour import Color


class ColorCam:
	camera = 0 #PiCamera()
	rawCapture = 0
	width = 640
	height = 480
	resolution=(width,height)
	sample_dimension = 14
	sample_cnt = (sample_dimension*2)**2
	thickness=4
	overlay = 0
	overlay_img = 0
	preview = 0
	window = 0
	default_color = Color("black")
	scan_coord_list = []
	def __init__(self):
		self.camera = PiCamera()
		self.camera.resolution = self.resolution
		self.camera.framerate = 32
		self.window = (0,0,self.width,self.height)
		self.preview = self.camera.start_preview(fullscreen=False,window=self.window)
		# adding overlay for selection box
		# transparent image
		
		with PiRGBArray(self.camera,size=self.resolution) as stream:
			self.camera.capture(stream,format="bgr",use_video_port=True)
	def add_overlay(self,tgt_x,tgt_y):
			# create image
			start_coord = (int(tgt_x-self.sample_dimension),int(tgt_y-self.sample_dimension))
			end_coord = (int(tgt_x+self.sample_dimension),int(tgt_y+self.sample_dimension))
			print("add_overlay",start_coord,end_coord)
			tgt_img_file = "picamcd/white_square.png"
			img_a = np.full((self.height,self.width,4),(255,255,255,128),dtype=np.uint8)
			res_img = cv2.rectangle(img_a,start_coord,end_coord,(0,0,0,255),4)
			cv2.imwrite(tgt_img_file,res_img)
			tgt_ol_img = cv2.imread(tgt_img_file)
			self.overlay = self.camera.add_overlay(tgt_ol_img,alpha=128,layer=3)
			self.overlay.fullscreen=False
			self.overlay.window = self.window

	def set_default_color(self,tgt_color):
		print(tgt_color)
		self.default_color = tgt_color
	def get_default_color(self):
		return self.default_color
	def get_color(self,tgt_x,tgt_y):
		with PiRGBArray(self.camera,size=self.resolution) as stream:
			self.camera.capture(stream,format="bgr",use_video_port=True)
			image = stream.array
			img = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
			rows,cols,_ = img.shape
			# check the array
			color_b = 0
			color_g = 0
			color_r = 0
			color_n = 0
			for currow in range(int(tgt_y-self.sample_dimension),int(tgt_y+self.sample_dimension)):
				for curcol in range(int(tgt_x-self.sample_dimension),int(tgt_x+self.sample_dimension)):
					cur_pixel = img[currow,curcol]
					if cur_pixel[0]+cur_pixel[1]+cur_pixel[2]>0:
						color_r += cur_pixel[2]
						color_g += cur_pixel[1]
						color_b += cur_pixel[0]
			sample_color = list((int(color_r/self.sample_cnt)/255,int(color_g/self.sample_cnt)/255,int(color_b/self.sample_cnt)/255))
			# return color
			sample_color = sample_color[::-1]
			# save as overlay img
			return Color(rgb=tuple(sample_color))
	def set_overlay_img(self,tgt_x,tgt_y,tgt_color):
		start_coord = (int(tgt_x-self.sample_dimension),int(tgt_y-self.sample_dimension))
		end_coord = (int(tgt_x+self.sample_dimension),int(tgt_y+self.sample_dimension))
		img_a = np.full((self.height,self.width,4),(0,0,0,255),dtype=np.uint8)
		ret_list = [element*255 for element in tgt_color.rgb] + [255]
		ret_list = tuple(ret_list)
		self.overlay_img = cv2.rectangle(img_a,start_coord,end_coord,ret_list,4)
