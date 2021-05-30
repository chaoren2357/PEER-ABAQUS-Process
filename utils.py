#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
utils.py
-------------------------
utils for the project
"""

import pickle


def load_pkl(addr):
    with open(addr,'rb') as fo:
        return pickle.load(fo) 
def save_pkl(content,addr,is_print = False):
    with open(addr,'wb') as fo:
        pickle.dump(content,fo)
    if is_print:
        print("finish saving ",addr)
def save_txt(content,addr = 'output.txt'):
	with open(addr,'wb') as f:
		f.write(content)
def read_file(addr):
	with open(addr,'r') as f:
		return f.read()
def get_format_time(*args):
    if len(args) == 1:
        during = args[0]
    elif len(args) == 2:
        during = args[1] - args[0]
    else:
        raise ValueError
    h = during//3600
    m = (during-h*3600)//60
    sec = during-h*3600-m*60
    return str(int(h)).zfill(3),str(int(m)).zfill(2),str(int(sec)).zfill(2) 