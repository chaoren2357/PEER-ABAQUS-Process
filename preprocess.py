#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
preprocess.py
-------------------------
generate modelXXX.inp to be the input file of abaqus

"""


import os
from utils import *

def create_model_inp(idx,seismic_data,addr = "Models"):
	'''change model_sample.inp into modelXXX.inp file, the main difference is the seismic data part.
	input:
	 - idx: int, the id of this model
	 - seismic_data: list, a list full of seismic data,e.g. [(0.2,0.04),(0.4,0.08)]
	 - addr: the root folder of modelXXX.inp, default "Models"
	output:
	  None
	'''

	model_path = os.path.join(addr,"model"+str(idx).zfill(3)+'.inp')

	# read the template file model_sample.inp
	with open(os.path.join(addr,"model_sample.inp"),'r') as f:
		data = f.readlines()

	# split the data into 3 blocks and only change the middle one
	start_content_id,end_content_id = -1,-1
	for idx,line in enumerate(data):
		if "*Amplitude" in line:
			start_content_id = idx
			continue
		if start_content_id != -1 and line[0] == '*':
			end_content_id = idx
			break
	data_prev = data[:start_content_id+1]
	data_next = data[end_content_id:]
	data_process = ""

	# generate the middle part from seismic_data
	for idx,(x,y) in enumerate(seismic_data):
		if idx%4 ==3:
			data_process+="        {:.3f},        {:f}\n".format(x,y)
		else:
			data_process+="        {:.3f},        {:f},".format(x,y)

	# output the modelXXX.inp
	output = "".join(data_prev)+data_process+"".join(data_next)
	with open(model_path,'w') as f:
		f.write(output)

def extract_seismic_data(filepath):
	'''extract seismic data from the orignial file from PEER database
	input:
	 - filepath: str, the path of PEER ground motion data
	output:
	 - res: list, the seismic data list in format [(time_{i},amplitude_{i}),(time_{i+1},amplitude_{i+1})].
	'''

	with open(filepath,'r') as f:
		str_data = f.readlines()
	start_content_id,end_content_id = -1,-1
	for idx,line in enumerate(str_data):
		if "SEC" in line:
			start_content_id = idx
			break
	deltaT_start_id = str_data[start_content_id].find("DT=")+3
	deltaT_end_id = str_data[start_content_id].find("SEC")
	deltaT = float(str_data[start_content_id][deltaT_start_id:deltaT_end_id])
	amplitude = []
	for line in str_data[start_content_id+1:]:
		for str_num in line.split():
			amplitude.append(float(str_num))

	res = []
	for i in range(len(amplitude)):
		res.append(((i+1)*deltaT,amplitude[i]))
	return res



def main():

	## init for id_wavename_map
	id_wavename_map_path = 'Result/id_wavename_map.pkl'
	if os.path.isfile(id_wavename_map_path):
		id_wavename_map = load_pkl(id_wavename_map_path)
	else:
		id_wavename_map = {}

	wavename_map_list = [v for _,v in id_wavename_map.items()]
	start_id = len(wavename_map_list)
	wavename_id_map = {wavename:idx for idx,wavename in id_wavename_map.items()}

	## init for id_data_map
	id_data_map_path = 'Result/id_data_map.pkl'
	if os.path.isfile(id_data_map_path):
		id_data_map = load_pkl(id_data_map_path)
	else:
		id_data_map = {}

	## find all proper files and process
	for root,dirs,files in os.walk("Data"):
		for filename in files:
			if ".AT2" in filename and "UP" not in filename:
				wavename = root.split('\\')[-1]+"@"+filename

				## id_wave_map process
				if wavename not in wavename_map_list:
					id_wavename_map[start_id] = wavename
					wavename_id_map[wavename] = start_id
					start_id+=1

				## id_data_map process
				idx = wavename_id_map[wavename]
				if idx not in id_data_map:
					seismic_data = extract_seismic_data(os.path.join(root,filename))
					create_model_inp(idx,seismic_data)
					id_data_map[idx] = seismic_data
	## save data
	save_pkl(id_wavename_map,id_wavename_map_path)
	save_pkl(id_data_map,id_data_map_path)



def play_around():
	with open('Models/model_sample.inp','r') as f:
		data = f.readlines()
	start_content_id,end_content_id = -1,-1
	for idx,line in enumerate(data):
		if "*Amplitude" in line:
			start_content_id = idx
			continue
		if start_content_id != -1 and line[0] == '*':
			end_content_id = idx
			break
	data_prev = data[:start_content_id+1]
	data_next = data[end_content_id:]
	data_procecss = [line.split() for line in data[start_content_id+1:end_content_id]]
	for line in data[start_content_id+1:end_content_id]:
		print(line)

def get_deltaT():
	data = load_pkl("Result/id_data_map.pkl")
	for idx,value in data.items():
		t_list = [t for t,A in value]
		t_list.sort()
		print(idx,round(t_list[1] - t_list[0],3))
def test():
		## Check exist res_dict
	res_path = "Result"
	data = load_pkl("Result/res_dict.pkl")
	for idx,(k,v) in enumerate(data.items()):
		print(v)
		break

if __name__ == '__main__':
	test()
	# get_deltaT()
	# play_around()