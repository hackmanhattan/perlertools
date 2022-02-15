def color_wheel(tgt_radius,tgt_color_list):
	# number of points in circle separation
	separation_degrees = int(360/len(tgt_color_list))
	print(separation_degrees)
	mp_x = screen_width/2
	mp_y = screen_height/2
	for i in range(len(tgt_color_list)):
		cur_angle = i * separation_degrees*(math.pi/180)
		cur_x = mp_x - math.sin(cur_angle)*tgt_radius
		cur_y = mp_y - math.cos(cur_angle)*tgt_radius
		print(i * separation_degrees, tgt_color_list[i].rgb)
		pygame.draw.circle(DISPLAY,hex_tuple(tgt_color_list[i]),(cur_x,cur_y),5)
