import numpy as np
import cv2

img_h = 480
img_w = 640

sample_dimension = 16

start_coord = (int((img_w/2)-sample_dimension),int((img_h/2)-sample_dimension))
end_coord = (int((img_w/2)+sample_dimension),int((img_h/2)+sample_dimension))

#sample_img = cv2.imread("sample.png")

def main():
	transparent_img = np.zeros((img_h,img_w,4),dtype=np.uint8)
	res_img = cv2.rectangle(transparent_img,start_coord,end_coord,(0,0,0),4)
	cv2.imwrite("./zero_square.png",res_img)

def white_square():
	img_a = np.zeros([img_h,img_w,1],dtype=np.uint8)
	img_a.fill(255)
	res_img = cv2.rectangle(img_a,start_coord,end_coord,(0,0,0),4)
	cv2.imwrite("./white_square.png",res_img)

white_square()
