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

def datacheck(inpfile_path,logger = None):
	name = os.path.splitext(os.path.basename(inpfile_path))[0]
	cmd_check = "abaqus job={} datacheck memory='10 gb'".format(name)
	status_check = os.system(cmd_check)
	return status_check



def calculate(inpfile_path,logger = None):
	name = os.path.splitext(os.path.basename(inpfile_path))[0]
	cmd_calculate = "abaqus job={} continue memory='10 gb'".format(name)
	status_calculate = os.system(cmd_calculate)
	return status_calculate




def calculate_inpy(inpfile_path,logger = None):
	modelName = os.path.splitext(os.path.basename(inpfile_path))[0]
	jobName = os.path.splitext(os.path.basename(inpfile_path))[0]
	myModel = mdb.ModelFromInputFile(modelName, inpfile_path)
	myJob = mdb.Job(name=jobName, model=modelName,numDomains=120,numCpus=12)# ,environment = (('node1','12'),))
	# Wait for the job to complete.
	myJob.submit()
	myJob.waitForCompletion()

def readODB(odbfile_path,logger = None):
	res_dict = {}
	odb = openOdb(path=odbfile_path)
	for stepName in odb.steps.keys():
		step = odb.steps[stepName]
		for regionName in step.historyRegions.keys():
			region = step.historyRegions[regionName]
			res_dict[regionName] = {}
			for phyQuant in region.historyOutputs.keys():
				res_dict[regionName][phyQuant] = []
				for t,dat in region.historyOutputs[phyQuant].data:
					res_dict[regionName][phyQuant].append(dat)
	return res_dict

def main():
	logger = Logger()
	# if not os.path.isdir('job_list'):
	# 	logger.debug("There is no job_list folder. You should run preprocess.py first.")
	# 	return 
	all_file = list(glob.glob('*.inp'))

	for idx,inpfile_path in enumerate(all_file):
		name = os.path.splitext(os.path.basename(inpfile_path))[0]

		# logger.debug("Start datacheck {} >>".format(name))
		# datacheck(inpfile_path,logger)
		# logger.debug("End datacheck {} <<".format(name))

		logger.debug("Start calculate {} >>".format(name))
		calculate(inpfile_path,logger)
		logger.debug("End calculate {} <<".format(name))

		# odbfile_path= name + '.odb'
		# logger.debug("Start saving the result of {} >>".format(name))
		# res_dict = readODB(odbfile_path)
		# save_json(res_dict,'{}.json'.format(name))
		# logger.debug("End saving the result of {} <<".format(name))

		
		if idx % int(0.1*len(all_file))== 0:
			logger.debug("{} files left".format(len(all_file)-idx-1))




				

def past():

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
