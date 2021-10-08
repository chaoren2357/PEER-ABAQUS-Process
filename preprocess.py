#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
preprocess.py
-------------------------
generate jobs from resource

"""


import os
from utils import *
from pathlib import Path
from tqdm import tqdm

def extract_seismic_data(filepath):
	'''extract seismic data from the dat file
	input:
	 - filepath: path of seismic data dat file
	output:
	 - dict:{
		name: str, file name;
		data: list, the seismic data list in format [(time_{i},amplitude_{i}),(time_{i+1},amplitude_{i+1})];
		deltaT: float, interval of seismic data.
	 }
	 
	'''
	with open(filepath,'r') as f:
		data_raw_list = f.read().split('\n')

	deltaT = 0.02
	data_list = [];data_str =""

	for i,dat_str in enumerate(data_raw_list):
		if dat_str == '':
			continue
		t = round(i*deltaT,2)
		dat = float(dat_str)
		data_list.append((t,dat))
		data_str+="        {:.2f},        {:.5f},".format(t,dat)
		if i%4 == 3:
			data_str += '\n'

	seismic_data = {
		'name': filepath.stem,
		'data_list': data_list,
		'data_str': data_str,
		'deltaT':deltaT,
		'dynamic_str': "{},{},".format(deltaT,data_list[-1][0])
	}
	return seismic_data

def extract_model_data(filepath):
	with open(filepath,'r') as f:
		data_list = f.readlines()
	spflag1,spflag2,spflag3 = -1,-1,-1
	for idx,content in enumerate(data_list):
		if '*Amplitude, name=Amp-ear' in content or '*Amplitude, name=AMP-EAR' in content:
			spflag1 = idx + 1
			continue
		if spflag1 != -1 and '*' in content and spflag2 == -1:
			spflag2 = idx
			continue
		if "*Dynamic" in content and spflag3 == -1:
			spflag3 = idx + 1
			continue

	# part1-seismic-part2-Dynamic-part3
	model_data = {
		'name': filepath.stem,
		'part1': ''.join(data_list[:spflag1]),
		'part2': ''.join(data_list[spflag2:spflag3]),
		'part3': ''.join(data_list[spflag3+1:]),
	}
	return model_data

def create_jobfile(model_data,seismic_data,filefolder):
	'''generate inp file using seismic data from seismic_data folder and model from model folder. 
	input:
	- model_str: str, the string of model file
	- seismic_data: dict, data from function extract_seismic_data
	output:
	  bool
	'''
	try:

		job = model_data['part1'] + seismic_data['data_str'] + '\n' + model_data['part2'] + seismic_data['dynamic_str'] + '\n' + model_data['part3']
		name = model_data['name']+'@'+seismic_data['name'] 
		filename = name + '.inp'
		with open(filefolder/ filename,'w') as f:
			f.write(job)
		return True,name
	except:
		return False,name

def main():
	logger = Logger()
	modelpath = Path('resource/model')
	seismicpath = Path('resource/seismic_data')
	bad_names = []
	for seipth,modelpth in tqdm([(seipth,modelpth) for seipth in list(seismicpath.glob('**/*.dat')) for modelpth in list(modelpath.glob('**/*.inp'))]):
		seismic_data = extract_seismic_data(seipth)
		model_data = extract_model_data(modelpth)
		flag,name = create_jobfile(model_data,seismic_data,Path('job_list'))
		if not flag:
			bad_names.append(name)
	print("bad:",bad_names)

if __name__ == '__main__':
	main()















