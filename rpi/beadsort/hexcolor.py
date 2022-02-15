from colour import Color

def hex_tuple(tgt_color):
	return [element*255 for element in tgt_color.rgb]

def hex_tuple_alpha(tgt_color):
	ret_list = [element*255 for element in tgt_color.rgb]
	ret_list += [255]
	return ret_list
def get_difference(tgt_color_a,tgt_color_b):
	print(tgt_color_a,tgt_color_b)
	res = 0
	for i in range(3):
		res += (tgt_color_a.rgb[i] - tgt_color_b.rgb[i])**2
	return res ** 0.5
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
