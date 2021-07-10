# PEER-ABAQUS-Process
**PEER-ABAQUS-Process** can help you process the origin [PEER Ground Motion Database](http://ngawest2.berkeley.edu) into a format dictionary and calculate the response of your model under these circumstances.

# Usage

- Install Abaqus 2016

- Clone repo

  ```python
  $ git clone https://github.com/chaoren2357/PEER-ABAQUS-Process.git
  $ cd PEER-ABAQUS-Process-master
  ```

- Add folder under `Models` folder with your own project name, e.g. `ThreeLayersFrame`, and modify the `projectNames =  ["ThreeLayersName","FiveLayersName"]` into your project name in `main` function of `preproccess.py` and `autoRun.py`.

- Rename your model to `model_sample.inp` and replace the original `Models/YourProjectName/model_sample.inp`.

- In your normal command(e.g. Anaconda Prompt), run `preprocess.py`

    ```python
    $ python preprocess.py
    ```
    
    Then, you can see that `modelXXX.inp` files are under `Models/YourProjectName/`
    
- In Abaqus command, run `autoRun.py`

    ```python
    $ abaqus cae noGUI=autoRun.py
    ```
    
    While running, you can check the log in `Result/YourProjectName/log.txt`
    
    The results are  `Result/YourProjectName/res_dict_XXX.pkl`

# Folder Structure

```
PEER-ABAQUS-Process
    │
    ├── Data (Data from PEER Ground Motion Database)
    │   ├── Borrego
    │   ├── Humbolt Bay
    │   ├── ...
    │
    ├── Models (Input models of Abaqus)
    │   ├── ThreeLayersFrame (project name)
    │       ├── model_sample.inp 
    │       ├── model000.inp 
    │       ├── model001.inp
    |       ├── ...
    │
    ├── Result (The output file of process)
    │   ├── ThreeLayersFrame 
    │       ├── id_data_map.pkl
    │       ├── id_wavename_map.pkl
    │       ├── log.txt
    |       ├── res_dict_00.pkl
    │       ├── res_dict_01.pkl
    |       ├── ...    
    ├── utils.py   
    ├── preprocess.py 
    ├── autoRun.py
    ├── check.py 
```

File Description
===============

- `id_data_map` is a python dictionary that contains the id---seismic wave data map. 

  seismic wave data is a list full of sample points, in (time,amplitude) format.

  e.g. 

	```
  keys: 0,1,2,3,4,....
  values:[(0.005, 0.0002188201), (0.01, 0.0002188683), (0.015, 0.0002189102),...],...
	```
- `id_wavename_map` is a python dictionary that contains the id---seismic wave name. 

  seismic wave name is a list full of strings, in "root@fileName" format.

  e.g. 

	```
  keys: 0,1,2,3,4,....
  values:"Borrego@RSN9_BORREGO_B-ELC000.AT2","Borrego@RSN9_BORREGO_B-ELC090.AT2",...
	```
- `res_dict_XXX` is a python dictionary that contains the Node --- Amplitude data. 

  Node is a string in "id@stepName@regionName@pointName" format.
  Amplitude data is almost the same as seismic wave data.

  e.g. 

	```
  keys: '0@Step-1@Node PART-1-1.100@A1', '0@Step-1@Node PART-1-1.101@A1', '0@Step-1@Node PART-1-1.102@A1',...
  values:((0.0, 0.0), (0.0199999995529652, 0.000782696530222893), (0.0399999991059303, 0.00512317474931479),(0.0599999986588955, -0.0077408947981894),...)

Attention that the output file in in the save interval and total time with the input seismic data.

License
=======

MIT License
