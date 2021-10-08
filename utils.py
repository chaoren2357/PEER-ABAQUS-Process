#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
utils.py
-------------------------
utils for the project
"""

import time
import json
import logging
import os
import glob
class Logger():
    def __init__(self,log_name = 'debug.log'):
        logging.basicConfig(filename=log_name,level=logging.DEBUG,format='%(asctime)s %(levelname)s:%(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        self.s_flag = False

    def debug(self,content):

        if ">>" in content:
            self.s = time.time()
            self.s_flag = True
        elif "<<" in content:
            if self.s_flag:
                during = time.time() - self.s
                hour = during//3600
                minute = (during-hour*3600)//60
                sec = during-hour*3600-minute*60
                content += ". Using time {:>2n}:{:>2n}:{:>2n}.".format(hour,minute,int(sec))
                self.s_flag = False
            else:
                logging.debug("Can not recongnize timer end flag")
                self.s_flag = False
        logging.debug(content)



def main():
    print()





def save_json(content,addr):
    with open(addr, "w") as f:
        json.dump(content, f, indent=4)  # 传入文件描述符，和dumps一样的结果

def save_txt(content,addr = 'output.txt'):
	with open(addr,'wb') as f:
		f.write(content)
def read_file(addr):
	with open(addr,'r') as f:
		return f.read()


if __name__ == '__main__':
    main()
