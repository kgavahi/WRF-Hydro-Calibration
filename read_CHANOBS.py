import numpy as np
import os
from netCDF4 import Dataset

def read_CHANOBS(path):
	
	files = os.listdir(path)
	files = [x for x in files if x.endswith('CHANOBS_DOMAIN1')]
	files = sorted(files)
	streamflows = np.zeros([len(files),5])
	c=0
	for file in files:
		path_file = os.path.join(path,file)
		f_CHANOPS = Dataset(path_file,'r')
		streamflow = f_CHANOPS.variables["streamflow"][:]
		streamflows[c,0] = int(file[:12])
		streamflows[c,1:5] = streamflow
		f_CHANOPS.close()
		c+=1

	np.savetxt(path+'/streamflows.csv',streamflows,delimiter=',')
	return streamflows

#path = '/mh1/kgavahi/WRF_Calibration'
#read_CHANOBS(path)