from abaqus import *
from abaqusConstants import *
import job
import visualization
from odbAccess import *
from utils import *
import os
import time

def main():
	res_path = "Result/res_dict.pkl"
	if os.path.isfile(res_path):
		res_dict = load_pkl(res_path)
	else:
		res_dict = {}
	with open("Result/log.txt",'a') as f:
		f.write("Start running at {}\n".format(time.asctime( time.localtime(time.time()) )))
	for waveid in [3,7,14]:
		s = time.time()
		modelName = 'model'+ str(waveid).zfill(3)
		jobName = 'job'+ str(waveid).zfill(3)

		myModel = mdb.ModelFromInputFile("ThreeLayerFrame", "Models/"+modelName+".inp")
		myJob = mdb.Job(name=jobName, model='ThreeLayerFrame',description='Three Layer Frame seismic design')

		# Wait for the job to complete.
		myJob.submit()
		myJob.waitForCompletion()

		odb = openOdb(path=jobName + '.odb')
		for stepName in odb.steps.keys():
			step = odb.steps[stepName]
			for regionName in step.historyRegions.keys():
				region = step.historyRegions[regionName]
				for pointName in region.historyOutputs.keys():
					data = region.historyOutputs[pointName].data
					key = "{}@{}@{}@{}".format(waveid,stepName,regionName,pointName)
					if key not in res_dict:
						res_dict[key] = data

		save_pkl(res_dict,"Result/res_dict.pkl")
		e = time.time()
		ht,mt,st = get_format_time(s,e)
		with open("Result/log.txt",'a') as f:
			f.write("Finish {},using time {}:{}:{}\n".format(modelName,ht,mt,st))
		myJob.kill()
		odb.close()

if __name__ == '__main__':
	main()
