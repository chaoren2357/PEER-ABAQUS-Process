#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
check.py
-------------------------
unnessesary file, you can motify it to check whether your output is correct.
"""

from abaqus import *
from abaqusConstants import *
import job
import visualization
from odbAccess import *
from utils import *
import os
import time

def main():
	log_project_path = "log.txt"

	# create name for model and job
	modelName = '0xiaomen'
	jobName = '0xiaomen'
	model_path = '0xiaomen.inp'

	## log file init
	with open(log_project_path,'a') as f:
		f.write("Start running at {}\n".format(time.asctime( time.localtime(time.time()) )))

	s = time.time()

	myModel = mdb.ModelFromInputFile(modelName, model_path)
	myJob = mdb.Job(name=jobName, model=modelName,description='seismic design')

	# Wait for the job to complete.
	myJob.submit()
	myJob.waitForCompletion()
	e = time.time()
	ht,mt,st = get_format_time(s,e)
	with open(log_project_path,'a') as f:
		f.write("Finish {} calculating,using time {}:{}:{}\n".format(modelName,ht,mt,st))
	# open result odb file
	res_dict = {}
	odb = openOdb(path=jobName + '.odb')
	for stepName in odb.steps.keys():
		step = odb.steps[stepName]
		for regionName in step.historyRegions.keys():
			region = step.historyRegions[regionName]
			for pointName in region.historyOutputs.keys():
				data = region.historyOutputs[pointName].data
				key = "{}@{}@{}@{}".format(modelName,stepName,regionName,pointName)
				with open(log_project_path,'a') as f:
					f.write("{}:{}\n".format(key,data))
				# add data into res_dict
				res_dict[key] = data

	# log
	e = time.time()
	ht,mt,st = get_format_time(s,e)
	with open(log_project_path,'a') as f:
		f.write("Finish {} saving,using time {}:{}:{}\n".format(modelName,ht,mt,st))

	## kill the job and close odb
	myJob.kill()
	odb.close()


if __name__ == '__main__':
	main()

