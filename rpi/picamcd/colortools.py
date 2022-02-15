import numpy as np
import cv2
from PIL import Image
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
	img_a = np.full((img_h,img_w,4),(0,0,0,255),dtype=np.uint8)
	res_img = cv2.rectangle(img_a,start_coord,end_coord,(255,255,255,255),4)
	cv2.imwrite("./white_square.png",res_img)

def transparent_square():
	img_a = np.full((img_h,img_w,4),(0,0,0,0),np.uint16)
	rgba = cv2.cvtColor(img_a, cv2.COLOR_RGB2RGBA)
	# img_a = np.zeros((img_h,img_w,4),np.uint8)
	# res_img = cv2.rectangle(img_a,start_coord,end_coord,(0,0,0,255),4)
	cv2.imwrite("./trans_square.png",cv2.cvtColor(img_a, cv2.COLOR_RGB2BGRA))

def transparent_pil():
	img = Image.new('RGBA', (img_w, img_h), (255, 0, 0, 0))
	# draw = ImageDraw.Draw(img)
	# draw.ellipse((25, 25, 75, 75), fill=(255, 0, 0))
	img.save('PIL_blank.png', 'PNG')
def stackoverflow():
		#create 3 separate BGRA images as our "layers"
	layer1 = np.zeros((500, 500, 4))
	layer2 = np.zeros((500, 500, 4))
	layer3 = np.zeros((500, 500, 4))

	#draw a red circle on the first "layer",
	#a green rectangle on the second "layer",
	#a blue line on the third "layer"
	red_color = (0, 0, 255, 255)
	green_color = (0, 255, 0, 255)
	blue_color = (255, 0, 0, 255)
	cv2.circle(layer1, (255, 255), 100, red_color, 5)
	cv2.rectangle(layer2, (175, 175), (335, 335), green_color, 5)
	cv2.line(layer3, (170, 170), (340, 340), blue_color, 5)

	res = layer1[:] #copy the first layer into the resulting image

	#copy only the pixels we were drawing on from the 2nd and 3rd layers
	#(if you don't do this, the black background will also be copied)
	cnd = layer2[:, :, 3] > 0
	res[cnd] = layer2[cnd]
	cnd = layer3[:, :, 3] > 0
	res[cnd] = layer3[cnd]

	cv2.imwrite("out.png", res)
def cv2_convert():
	tgt_file = "./cv2writeb.png"
	img_a = cv2.imread(tgt_file,cv2.IMREAD_UNCHANGED)
	print(img_a.shape)
	rows,cols,_= img_a.shape
	for i in range(rows):
		for j in range(cols):
			img_a[i][j] = [0,255,0]
	# res_img = cv2.resize(img_a,(img_w,img_h),interpolation = cv2.INTER_AREA)
	# res_img = cv2.rectangle(img_a,start_coord,end_coord,(0,0,0,255),4)
	cv2.imwrite("cv2writed.png",img_a)
def convert_img():
	tgt_img_file = "./cv2writeb.png"
	image = Image.open(tgt_img_file)
	image.convert("P")
	print(image)
	print("mode",image.mode)
	newImage = []
	cnt_a = 0
	cnt_b = 0
	for item in image.getdata():
		# newImage.append((0, 255, 255, 0))
		if item[:3] == (255, 255, 255):
			cnt_a += 1
			newImage.append((0, 255, 255, 0))
		else:
			cnt_b += 1
			newImage.append(item)
		# Convert to mode 'P', and apply palette as flat list
	print(cnt_a,cnt_b)
	image.putdata(newImage)
	# img_pil = image.convert('P')

	# Save indexed image for comparison
	image.save('output_indexed.png')
	print(image.mode, image.size)

def merge_img():
	# why does this work
	background = cv2.imread('./sample.png')
	overlay = cv2.imread('./white_square.png')

	added_image = cv2.addWeighted(background,1.0,overlay,1,0)

	cv2.imwrite('combined.png', added_image)

white_square()
# transparent_square()
# cv2_convert()
# convert_img()
merge_img()
# transparent_pil()
# stackoverflow()
