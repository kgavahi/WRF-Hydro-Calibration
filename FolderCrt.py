import numpy as np
import os
import shutil


RUN = 'RUN'
p_size = 6
Mian_path = '/mh1/kgavahi/WRF_Calibration'

if os.path.exists('./CALIB_OUT'):
	shutil.rmtree('./CALIB_OUT')
	os.mkdir('./CALIB_OUT')
	os.mkdir('./CALIB_OUT/plots')
	os.mkdir('./CALIB_OUT/BEST_DOMAIN')
else:
	os.mkdir('./CALIB_OUT')
	os.mkdir('./CALIB_OUT/plots')
	os.mkdir('./CALIB_OUT/BEST_DOMAIN')

if not os.path.exists(RUN):      # Create directory for open-loop model run
    os.makedirs(RUN)

folder = RUN
for the_file in os.listdir(folder):     # Delete the content of 'Open_Loop+ '/Open_%03d'  
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)

for i in range(1,(p_size+1)):     
    path = os.path.join(RUN, 'P_%03d' %i)

    if not os.path.exists(path):
        os.makedirs(path)

for i in range(1,(p_size+1)):     
    path = os.path.join(RUN, 'P_%03d' %i)
    dst = os.path.join(path, 'DOMAIN')
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(dst):
        os.makedirs(dst)
    if not os.path.exists(os.path.join(path, 'Output')):
        os.makedirs(os.path.join(path, 'Output'))
    if not os.path.exists(os.path.join(path, 'RESTART')):
        os.makedirs(os.path.join(path, 'RESTART'))

# Copy namelist.hrldas and other required files to each Run folder in Open_%03d
for i in range(1,(p_size+1)): 	
	path = os.path.join(RUN, 'P_%03d' %i)

    
	file_CHANPARM        = os.path.join(Mian_path, 'CHANPARM.TBL')
	file_namelist_hydro  = os.path.join(Mian_path, 'hydro.namelist')
	file_namelist_hrldas = os.path.join(Mian_path, 'namelist.hrldas')
	file_soilparm        = os.path.join(Mian_path, 'SOILPARM.TBL')
	file_mptable         = os.path.join(Mian_path, 'MPTABLE.TBL')
	file_genparm         = os.path.join(Mian_path, 'GENPARM.TBL')
	file_hrldas          = os.path.join(Mian_path, 'wrf_hydro.exe')
	file_hydroTBL          = os.path.join(Mian_path, 'HYDRO.TBL')
	
	shutil.copy(file_CHANPARM,path)
	shutil.copy(file_namelist_hydro,path)
	shutil.copy(file_namelist_hrldas,path)
	shutil.copy(file_soilparm,path)
	shutil.copy(file_mptable,path)
	shutil.copy(file_genparm,path)
	shutil.copy(file_hrldas,path)
	shutil.copy(file_hydroTBL,path)
	

	src = os.path.join(Mian_path, 'DOMAIN')
	dst = os.path.join(path, 'DOMAIN')
    
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlinks=False, ignore=None)
		else:
			shutil.copy2(s, d)


	src = os.path.join(Mian_path, 'RESTART')
	dst = os.path.join(path, 'RESTART')
    
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlinks=False, ignore=None)
		else:
			shutil.copy2(s, d)
