import os
from utils import *

def create_model_inp(idx,seismic_data,addr = "Models"):
	model_path = os.path.join(addr,"model"+str(idx).zfill(3)+'.inp')
	with open(os.path.join(addr,"model_sample.inp"),'r') as f:
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
	data_process = ""
	for idx,(x,y) in enumerate(seismic_data):
		if idx%4 ==3:
			data_process+="        {:.3f},        {:f}\n".format(x,y)
		else:
			data_process+="        {:.3f},        {:f},".format(x,y)

	output = "".join(data_prev)+data_process+"".join(data_next)
	with open(model_path,'w') as f:
		f.write(output)

def extract_seismic_data(filepath):

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


if __name__ == '__main__':
	main()
	# play_around()