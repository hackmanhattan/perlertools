import cv2

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy

camera = PiCamera()
resolution=(640,480)
camera.resolution = resolution
camera.framerate = 32
rawCapture = PiRGBArray(camera,size=resolution)

time.sleep(0.1)

sample_dimension = 16
start_coord = (int((resolution[0]/2)-sample_dimension),int((resolution[1]/2)-sample_dimension))
end_coord = (int((resolution[0]/2)+sample_dimension),int((resolution[1]/2)+sample_dimension))
thickness=4
sample_cnt = (sample_dimension*2)**2

def getColorFromImage(image):
	print("done")

def main():
	sample_color = (0,0,0)
	for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
		image = frame.array
		image_b = cv2.rectangle(image,start_coord,end_coord,sample_color,thickness)
		cv2.imshow("Frame",image_b)
		key = cv2.waitKey(1) & 0xFF
		rawCapture.truncate(0)
		if key == ord("q"):
			break
		if key == ord("c"):
			img = cv2.cvtColor(numpy.array(image),cv2.COLOR_RGB2BGR)
			rows,cols,_=img.shape
			# check the array
			color_b = 0
			color_g = 0
			color_r = 0
			color_n = 0
			for currow in range(int(rows/2-sample_dimension),int(rows/2+sample_dimension)):
				for curcol in range(int(cols/2-sample_dimension),int(cols/2+sample_dimension)):
					cur_pixel = img[currow,curcol]
					if cur_pixel[0]+cur_pixel[1]+cur_pixel[2]>0:
						color_r += cur_pixel[2]
						color_g += cur_pixel[1]
						color_b += cur_pixel[0]
			sample_color = (int(color_r/sample_cnt),int(color_g/sample_cnt),int(color_b/sample_cnt))

main()
