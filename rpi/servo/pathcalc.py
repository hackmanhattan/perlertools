import numpy as np

def get_path(init_x, tgt_x,tgt_round):
    ret_list = []
    print(init_x,tgt_x)
    if init_x > tgt_x: #towards graveyard
        ret_list += [round(curx*0.1,tgt_round) for curx in range(int(init_x*10),int(tgt_x*10),-1)]
    elif init_x<tgt_x: #towards filter
        ret_list += [round(curx*0.1,tgt_round) for curx in range(int(init_x*10),int(tgt_x*10))]
    return ret_list

def get_wiggle_path(init_x,tgt_x,tgt_round):
    # TODO: Make more elegant
    mov_list = []
    wiggle_diff = 0.3
    if init_x > tgt_x:
        mov_list += [round(curx*0.1,tgt_round) for curx in range(int(tgt_x*10),int((tgt_x-wiggle_diff)*10),-1)]
        mov_list += [round(curx*0.1,tgt_round) for curx in range(int((tgt_x-wiggle_diff)*10),int((tgt_x+wiggle_diff)*10))]
        mov_list += [round(curx*0.1,tgt_round) for curx in range(int((tgt_x+wiggle_diff)*10),int(tgt_x*10),-1)]
    if init_x < tgt_x:
        mov_list += [round(curx*0.1,tgt_round) for curx in range(int(tgt_x*10),int((tgt_x+wiggle_diff)*10))]
        mov_list += [round(curx*0.1,tgt_round) for curx in range(int((tgt_x+wiggle_diff)*10),int((tgt_x-wiggle_diff)*10),-1)]
        mov_list += [round(curx*0.1,tgt_round) for curx in range(int((tgt_x-wiggle_diff)*10),int(tgt_x*10),-1)]
    return mov_list