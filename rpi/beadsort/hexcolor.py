from colour import Color


def generate_circle_color(tgt_detail):
	#ret_list = [Color("black"),Color("red"),Color("green"),Color("blue"),Color("violet"),Color("yellow")]
	ret_list = [Color("black")]
	ret_list.append(Color("#040404"))	#,Color("#ffbddd")]
	ret_list.append(Color("#74c2de"))
	ret_list.append(Color("#fb91d5"))
	ret_list.append(Color("#d8dccd"))
	#,Color("#99e2fb"),Color("#111111")]
	for i in range(tgt_detail):
		cur_list = ret_list
		new_list = []
		cur_length = len(cur_list)
		for j in range(cur_length):
			new_list.append(cur_list[j])
			cur_mix_color = mix_color(cur_list[j],cur_list[(j+1)%cur_length])
			new_list.append(cur_mix_color)
		ret_list = new_list
	return ret_list
def get_closest_wheel_color(tgt_color,tgt_color_list):
	cur_idx = 0
	cur_diff = 1000.0
	for idx in range(1,len(tgt_color_list)):
		tmp_diff = get_difference(tgt_color,tgt_color_list[idx])
		if cur_diff > tmp_diff and tmp_diff <0.17:
			cur_diff = tmp_diff
			cur_idx = idx
	return cur_idx

def hex_tuple(tgt_color):
	return [element*255 for element in tgt_color.rgb]

def get_difference(tgt_color_a,tgt_color_b):
	res = 0
	for i in range(3):
		res += (tgt_color_a.rgb[i] - tgt_color_b.rgb[i])**2
	return res ** 0.5

def get_hsl_difference(tgt_color_a,tgt_color_b):
	# use hue
	return abs(tgt_color_a.hsl[0]-tgt_color_b.hsl[0])

def get_rgb(tgt_color_tuple):
	res = "#"
	for i in range(3):
		res+= hex(tgt_color_tuple[i]).replace("0x","")
	return res
def mix_color(tgt_color_a,tgt_color_b):
	res = []
	for i in range(3):
		cur_avg = (tgt_color_a.rgb[i]+tgt_color_b.rgb[i])/2
		res.append(cur_avg)
	return Color(rgb=tuple(res))
