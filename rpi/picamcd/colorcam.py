import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
from colour import Color
from PIL import Image


class ColorCam:
	camera = 0 #PiCamera()
	rawCapture = 0
	width = 640
	height = 480
	resolution=(width,height)
	sample_dimension = 16
	sample_cnt = (sample_dimension*2)**2
	thickness=2
	overlay = 0
	overlay_img = 0
	preview = 0
	window = 0
	default_color = Color("black")
	scan_coord_list = []
	viewport_img_array = 0
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
	def add_overlay(self):
		# create image
		self.overlay = self.camera.add_overlay(self.overlay_img,alpha=125,layer=3)
		self.overlay.fullscreen=False
		self.overlay.window = self.window
	def remove_overlay(self):
		self.camera.remove_overlay(self.overlay)
	def set_default_color(self,tgt_color):
		self.default_color = tgt_color
	def get_default_color(self):
		return self.default_color
	def save_img_locally(self):
		with PiRGBArray(self.camera,size=self.resolution) as stream:
			self.camera.capture(stream,format="bgr",use_video_port=True)
			image_arr = stream.array
			img = cv2.cvtColor(np.array(image_arr),cv2.COLOR_RGB2BGR)
			cv2.imwrite("test.png", img)
	def get_color(self,tgt_x,tgt_y,tgt_dimension):
		with PiRGBArray(self.camera,size=self.resolution) as stream:
			self.camera.capture(stream,format="bgr",use_video_port=True)
			image_arr = stream.array
			image_arr = image_arr[int(tgt_y -(tgt_dimension[1]/2)):int(tgt_y+(tgt_dimension[1]/2)),int(tgt_x -(tgt_dimension[0]/2)):int(tgt_x+(tgt_dimension[0]/2))]
			img = cv2.cvtColor(np.array(image_arr),cv2.COLOR_RGB2BGR)
			rows,cols,_ = img.shape
			# check the array
			color_b = 0
			color_g = 0
			color_r = 0
			color_n = 0
			total_pixel_cnt = tgt_dimension[0]*tgt_dimension[1]
			for currow in range(tgt_dimension[1]):
				for curcol in range(tgt_dimension[0]):
					cur_pixel = img[currow,curcol]
					if cur_pixel[0]+cur_pixel[1]+cur_pixel[2]>0:
						color_r += cur_pixel[2]
						color_g += cur_pixel[1]
						color_b += cur_pixel[0]
			sample_color = list((int(color_r/total_pixel_cnt)/255,int(color_g/total_pixel_cnt)/255,int(color_b/total_pixel_cnt)/255))
			# return color
			sample_color = sample_color[::-1]
			# save as overlay img
			ret_color = Color(rgb=tuple(sample_color))
			# print(ret_color)
			return ret_color
	def set_default_viewport(self,tgt_x,tgt_y,tgt_dimension):
		with PiRGBArray(self.camera,size=self.resolution) as stream:
			self.camera.capture(stream,format="bgr",use_video_port=True)
			image_arr = stream.array
			# main_img = cv2.cvtColor(np.array(image_arr),cv2.COLOR_RGB2BGR)
			# cv2.imwrite("test.png", main_img)
			image_arr = image_arr[int(tgt_y -(tgt_dimension[1]/2)):int(tgt_y+(tgt_dimension[1]/2)),int(tgt_x -(tgt_dimension[0]/2)):int(tgt_x+(tgt_dimension[0]/2))]
			# cv2.imwrite("testb.png", crop_img)
			self.viewport_img_array = image_arr
	def get_default_viewport_str(self):
		return self.viewport_img_array
	def get_refresh_vals(self,tgt_x,tgt_y,tgt_dimension):
		#returns color and comparison
		with PiRGBArray(self.camera,size=self.resolution) as stream:
			self.camera.capture(stream,format="bgr",use_video_port=True)
			cur_image_arr = stream.array
			cur_image_arr = cur_image_arr[int(tgt_y -(tgt_dimension[1]/2)):int(tgt_y+(tgt_dimension[1]/2)),int(tgt_x -(tgt_dimension[0]/2)):int(tgt_x+(tgt_dimension[0]/2))]

			avg_diff = 0
			color_b = 0
			color_g = 0
			color_r = 0
			color_n = 0
			total_pixel_cnt = tgt_dimension[0]*tgt_dimension[1]
			for currow in range(tgt_dimension[1]):
				for curcol in range(tgt_dimension[0]):
					cur_pixel = cur_image_arr[currow,curcol]
					vp_pixel = self.viewport_img_array[currow,curcol]
					cur_diff = 0
					for idxp in range(3):
						cur_diff += (vp_pixel[idxp]-cur_pixel[idxp])**2
					# print(currow,curcol,cur_pixel,vp_pixel,cur_diff)
					cur_diff = cur_diff ** 0.5
					avg_diff += cur_diff

					# print(currow,curcol,cur_pixel,vp_pixel,cur_diff)
					# math for sample color
					if cur_pixel[0]+cur_pixel[1]+cur_pixel[2]>0:
						color_r += cur_pixel[2]
						color_g += cur_pixel[1]
						color_b += cur_pixel[0]
			sample_color = list((int(color_r/total_pixel_cnt)/255,int(color_g/total_pixel_cnt)/255,int(color_b/total_pixel_cnt)/255))

			avg_diff = avg_diff/total_pixel_cnt
			avg_diff = round(avg_diff,5)
			# sample_color = sample_color[::-1]
			ret_color = Color(rgb=tuple(sample_color))
			return (ret_color,avg_diff)
	def set_overlay_img(self,tgt_x,tgt_y,tgt_dimension,tgt_color):
		start_coord = (int(tgt_x-(tgt_dimension[0]/2)),int(tgt_y-(tgt_dimension[1]/2)))
		end_coord = (int(tgt_x+(tgt_dimension[0]/2)),int(tgt_y+(tgt_dimension[1]/2)))
		ret_list = [element*255 for element in tgt_color.rgb] + [255]
		ret_list = tuple(ret_list)
		img_a = np.full((self.height,self.width,4),(255,0,0,0),dtype=np.uint8)
		res_img = cv2.rectangle(img_a,start_coord,end_coord,ret_list,2)
		self.overlay_img = res_img
	