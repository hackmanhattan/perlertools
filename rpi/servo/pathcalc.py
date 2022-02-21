import numpy as np

step_cnt = 5
def get_path(init_x, tgt_x,tgt_round):
    ret_list = []
    if init_x > tgt_x: #towards graveyard
        ret_list += [curx for curx in range(int(init_x),int(tgt_x),-1*step_cnt)]
    elif init_x<tgt_x: #towards filter
        ret_list += [curx for curx in range(int(init_x),int(tgt_x),step_cnt)]
    return ret_list

def get_wiggle_path(init_x,tgt_x,tgt_round):
    # TODO: Make more elegant
    mov_list = []
    wiggle_diff = 50
    
    if init_x > tgt_x:
        mov_list += [curx for curx in range(int(tgt_x),int((tgt_x-wiggle_diff)),-10)]
        mov_list += [curx for curx in range(int(tgt_x-wiggle_diff),int(tgt_x+wiggle_diff),10)]
        mov_list += [curx for curx in range(int(tgt_x+wiggle_diff),int(tgt_x),-10)]
    if init_x < tgt_x:
        mov_list += [curx for curx in range(int(tgt_x),int(tgt_x+wiggle_diff),10)]
        mov_list += [curx for curx in range(int(tgt_x+wiggle_diff),int(tgt_x-wiggle_diff),-10)]
        mov_list += [curx for curx in range(int(tgt_x-wiggle_diff),int(tgt_x),10)]
    return mov_list