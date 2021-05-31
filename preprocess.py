#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
preprocess.py
-------------------------
generate modelXXX.inp to be the input file of abaqus

"""


import os
from utils import *
from pathlib import Path




def create_model_inp(model_id,interval,seismic_data,project_model_path):
	'''change model_sample.inp into modelXXX.inp file, the main difference is the seismic data part.
	input:
	 - idx: int, the id of this model
	 - seismic_data: list, a list full of seismic data,e.g. [(0.2,0.04),(0.4,0.08)]
	 - addr: the root folder of modelXXX.inp, default "Models"
	output:
	  None
	'''

	model_path = project_model_path / "model{}.inp".format(str(model_id).zfill(3))
	template_path = project_model_path / "model_sample.inp"

	# read the template file model_sample.inp
	with open(template_path,'r') as f:
		data = f.readlines()

	# split the data into 3 blocks 
	start_content_id,end_content_id = -1,-1
	for idx,line in enumerate(data):
		if "*Amplitude" in line:
			start_content_id = idx
			continue
		if start_content_id != -1 and line[0] == '*':
			end_content_id = idx
			break
	data_prev = data[:start_content_id+1]
	data_process = ""
	data_next = data[end_content_id:]
	

	# change job name and model name in the first part
	for idx,line in enumerate(data_prev):
		if "JOB" in line or "Job" in line or "job" in line:
			newline = line.split()
			newline[3] = 'job'+ str(model_id).zfill(3)
			newline[6] = 'model'+ str(model_id).zfill(3)
			newline = ' '.join(newline) +'\n'
			data_prev[idx] = newline 
			break

	# generate the second part from seismic_data
	for idx,(x,y) in enumerate(seismic_data):
		if idx%4 ==3:
			data_process+="        {:.3f},        {:f}\n".format(x,y)
		else:
			data_process+="        {:.3f},        {:f},".format(x,y)

	# modify time interval and total time of step
	for idx,line in enumerate(data_next):
		if "*Dynamic" in line:
			timeId = idx +1
			break
	total_time = max([x for x,_ in seismic_data])
	data_next[timeId] = "{},{},\n".format(interval,total_time)

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
	return deltaT,res



def main():
	# basic informations
	projectNames = ['ThreeLayersFrame' ,'FiveLayersFrame']
	CUR_PATH = Path(__file__).absolute().parent
	RESULT_PATH = CUR_PATH / "Result"
	MODEL_PATH = CUR_PATH / "Models"
	DATA_PATH = CUR_PATH / "Data"

	for projectName in projectNames:
		project_result_path = RESULT_PATH / projectName
		project_model_path = MODEL_PATH / projectName

		if not project_model_path.is_dir():
			raise ValueError("Please check whether {} is in file Models".format(projectName))
		if not project_result_path.is_dir():
			project_result_path.mkdir()

		## init for id_wavename_map
		id_wavename_map_path = project_result_path / 'id_wavename_map.pkl'
		if id_wavename_map_path.is_file():
			id_wavename_map = load_pkl(id_wavename_map_path)
		else:
			id_wavename_map = {}

		wavename_map_list = [v for _,v in id_wavename_map.items()]
		current_id = len(wavename_map_list)
		wavename_id_map = {wavename:idx for idx,wavename in id_wavename_map.items()}

		## init for id_data_map
		id_data_map_path = project_result_path / 'id_data_map.pkl'
		if id_data_map_path.is_file():
			id_data_map = load_pkl(id_data_map_path)
		else:
			id_data_map = {}

		## find all proper files and process
		for root,dirs,files in os.walk(DATA_PATH):
			for filename in files:
				if ".AT2" in filename and "UP" not in filename:
					root_path = Path(root)
					wavename = root_path.name+"@"+filename

					## id_wave_map process
					if wavename not in wavename_map_list:
						id_wavename_map[current_id] = wavename
						wavename_id_map[wavename] = current_id
						current_id+=1

					## id_data_map process
					idx = wavename_id_map[wavename]
					if idx not in id_data_map:
						interval,seismic_data = extract_seismic_data(root_path / filename)
						id_data_map[idx] = seismic_data
						create_model_inp(idx,interval,seismic_data,project_model_path)
		## save data
		save_pkl(id_wavename_map,id_wavename_map_path)
		save_pkl(id_data_map,id_data_map_path)


if __name__ == '__main__':
	main()
