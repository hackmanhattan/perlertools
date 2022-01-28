from colour import Color

def hex_tuple(tgt_color):
	return [element*255 for element in tgt_color.rgb]

def mix_color(tgt_color_a,tgt_color_b):
	res = []
	for i in range(3):
		cur_avg = (tgt_color_a.rgb[i]+tgt_color_b.rgb[i])/2
		res.append(cur_avg)

	return Color(rgb=tuple(res))
