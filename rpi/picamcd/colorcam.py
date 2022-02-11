import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy


class ColorCam:
	camera = 0 #PiCamera()
	rawCapture = 0
	width = 640
	height = 480
	resolution=(640,480)
	sample_dimension = 16

	start_coord = (int((resolution[0]/2)-sample_dimension),int((resolution[1]/2)-sample_dimension))
	end_coord = (int((resolution[0]/2)+sample_dimension),int((resolution[1]/2)+sample_dimension))
	sample_cnt = (sample_dimension*2)**2
	thickness=4
	overlay = 0
	preview = 0
	def __init__(self):
		self.camera = PiCamera()
		self.camera.resolution = self.resolution
		self.camera.framerate = 32
		self.preview = self.camera.start_preview()
		# adding overlay for selection box
		# transparent image
		with PiRGBArray(self.camera,size=self.resolution) as stream:
			self.camera.capture(stream,format="bgr",use_video_port=True)
			image = stream.array
			image_b = cv2.rectangle(image,self.start_coord,self.end_coord,(0,0,0),self.thickness)
			tgt_ol_img = cv2.imread("white_square.png")
			self.overlay = self.camera.add_overlay(tgt_ol_img,layer=3,alpha=128)
	def getColor(self):
		with PiRGBArray(self.camera,size=self.resolution) as stream:
			self.camera.capture(stream,format="bgr",use_video_port=True)
			image = stream.array
			#cv2.imshow("Frame",image)
			#cv2.waitKey(0)
			img = cv2.cvtColor(numpy.array(image),cv2.COLOR_RGB2BGR)
			cv2.imwrite("sample.png",image)
			rows,cols,_ = img.shape
			# check the array
			color_b = 0
			color_g = 0
			color_r = 0
			color_n = 0
			for currow in range(int(rows/2-self.sample_dimension),int(rows/2+self.sample_dimension)):
				for curcol in range(int(cols/2-self.sample_dimension),int(cols/2+self.sample_dimension)):
					cur_pixel = img[currow,curcol]
					if cur_pixel[0]+cur_pixel[1]+cur_pixel[2]>0:
						color_r += cur_pixel[2]
						color_g += cur_pixel[1]
						color_b += cur_pixel[0]
			sample_color = (int(color_r/self.sample_cnt),int(color_g/self.sample_cnt),int(color_b/self.sample_cnt))
			return sample_color
