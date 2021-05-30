#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
check.py
-------------------------
unnessesary file, you can motify it to check whether your output is correct.
"""

import matplotlib.pyplot as plt
import pickle

def load_pkl(addr):
    with open(addr,'rb') as fo:
        return pickle.load(fo) 
def check():
	res_dict = load_pkl("Result/res_dict.pkl")
	for k,v in res_dict.items():
		print(len(v))
	# idx = 0
	# for k,v in res_dict.items():
	# 	xL = [x for x,y in v]
	# 	yL = [y for x,y in v]
	# 	plt.plot(xL,yL)
	# 	if idx == 5:
	# 		break
	# 	idx+=1
	# plt.show()

if __name__ == '__main__':
	check()