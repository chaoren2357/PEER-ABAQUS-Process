#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
autoRun.py
-------------------------
calculate all inp files with abaqus, and save output data

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

	projectNames = ['ThreeLayersFrame','FiveLayersFrame']
	for projectName in projectNames:

		result_project_path = os.path.join("Result",projectName)
		log_project_path = os.path.join("Result",projectName,"log.txt")
		models_project_path = os.path.join("Models",projectName)

		## check exist res_dict
		id_exist = []
		for _,_,files in os.walk(result_project_path):
			for filename in files:
				if filename[:8] == "res_dict":
					id_exist.append(filename[9:-4])

		## log file init
		with open(log_project_path,'a') as f:
			f.write("Start running at {}\n".format(time.asctime( time.localtime(time.time()) )))


		## find inp file id
		ids = []
		for _,_,files in os.walk(models_project_path):
			for filename in files:
				if filename[:5] == "model" and filename != 'model_sample.inp':
					ids.append(filename[5:-4])
		

		# iterate from all ids
		for waveid in ids:

			if waveid in id_exist:
				continue

			s = time.time()

			# create name for model and job
			modelName = 'model'+ str(waveid).zfill(3)
			jobName = 'job'+ str(waveid).zfill(3)
			model_path = os.path.join("Models",projectName,modelName+".inp")
			pkl_path = os.path.join("Result",projectName,"res_dict_{}.pkl".format(waveid))

			myModel = mdb.ModelFromInputFile(modelName, model_path)
			myJob = mdb.Job(name=jobName, model=modelName,description='{} seismic design'.format(projectName))

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
						key = "{}@{}@{}@{}".format(waveid,stepName,regionName,pointName)

						# add data into res_dict
						res_dict[key] = data

			save_pkl(res_dict,pkl_path)

			# log
			e = time.time()
			ht,mt,st = get_format_time(s,e)
			with open(log_project_path,'a') as f:
				f.write("Finish {} saving,using time {}:{}:{}\n".format(modelName,ht,mt,st))

			## kill the job and close odb
			myJob.kill()
			odb.close()

		with open(log_project_path,'a') as f:
			f.write("Finish all.............................................\n")

if __name__ == '__main__':
	main()
