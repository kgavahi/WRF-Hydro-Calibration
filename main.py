import pandas as pd
import numpy as np
import copy
import multiprocessing
import update_parameters as up
import FolderCrt
import os
from subprocess import *
from fitness import fitness
import matplotlib.pyplot as plt
import shutil
import plot

def __wrf__hydro__(i):
	path = os.path.join('RUN', 'P_%03d' %i)
	
	hrlds = Popen(['srun', '-u', '--mpi=pmi2', '-n', '7', '-p', 'mh1', '--qos', 'mh1', './wrf_hydro.exe'], 
	cwd = path, 
	close_fds=True,
	stdout=PIPE,
	preexec_fn=os.setsid,
	shell=False,
	stdin=DEVNULL)
	
	out, err = hrlds.communicate()
	kge = fitness(path)
	np.savetxt(path + '/kge.csv',[kge])
def PertX(P,X_best,X_min,X_max):
	X_new = copy.deepcopy(X_best)
	randi = np.random.rand(len(X_new))
	sel = P>randi
	if not any(sel):
		sel[round(np.random.rand()*(len(sel))-1)] = True
	print(sel)

	X_lower = X_min[sel]
	X_upper = X_max[sel]
	X_sel = X_new[sel]	

	for j in range(len(X_sel)):

		X_sel_new = X_sel[j] + r * (X_upper[j]-X_lower[j]) * np.random.randn()
		if X_sel_new<X_lower[j]:
			X_sel_new = X_lower[j] + (X_lower[j] - X_sel_new)
			if X_sel_new>X_upper[j]:
				X_sel_new = X_lower[j]
		if X_sel_new>X_upper[j]:
			X_sel_new = X_upper[j] - (X_sel_new - X_upper[j])
			if X_sel_new<X_lower[j]:
				X_sel_new = X_upper[j]
		X_sel[j] = X_sel_new
	
	X_new[sel] = X_sel	
	return X_new
	
	
	
	
BaseDir = './BASELINE_PARAMETERS'

	
file = 'calib_parms.tbl'

f = pd.read_csv(file,sep=',')


bool = np.array(f.calib_flag,dtype=bool)

index = f.index[bool]
X0 = np.array(f.ini[bool])
X_min = np.array(f.minValue[bool])
X_max = np.array(f.maxValue[bool])
ParamToChange = list(f.parameter[bool])
NewParameters = np.array(f.ini)


if __name__ == '__main__':
	r = 0.2
	max_iter = 150
	F_BEST_ALL = []
	for i in range(129,max_iter+1):
		
		print('\niter = ',i)
		if i==129:
			X_best = X0
			f_best = 3.11789
			
		
		P = 1 - np.log(i)/np.log(max_iter)
	
		#Prepare new parameters for 5 processes
		for process in range(1,7):
			f = pd.read_csv(file,sep=',')
			path_p = os.path.join('RUN', 'P_%03d' %process)
			X_new = PertX(P,X_best,X_min,X_max)
			print(X_new)
			NewParameters[index] = X_new
			f.insert(5,'adjusted',NewParameters,True)
			f.to_csv(path_p+'/Param_iter_%d.csv'%i)
			up.CHANupdate(BaseDir,path_p,ParamToChange,f)
			up.NcFilesUpdate(BaseDir,path_p,ParamToChange,f)	
		
		#Run 5 WRF_hydro in parallel
		pool = multiprocessing.Pool(processes = 6)
		pool.map(__wrf__hydro__, range(1,(6+1)))
		pool.close()	
		
		#Find the best process run
		kges = np.zeros([6])
		for process in range(1,7):
			path_p = os.path.join('RUN', 'P_%03d' %process)
			kges[process-1] = np.genfromtxt(path_p+'/kge.csv')
			os.rename(path_p+'/streamflows.csv',path_p+'/streamflows_%d.csv'%i)
			
		print('kges:',kges)
		id_best = np.argmax(kges)
		f_new = np.max(kges)
		print('id_best:',id_best,'f_new :',f_new)
		
		#Write the best process run into X_new
		path_best = os.path.join('RUN', 'P_%03d' %(id_best+1))
		fpBest = pd.read_csv(path_best+'/Param_iter_%d.csv'%i,sep=',')
		X_new = np.array(fpBest.adjusted[bool])
		print('X_new:',X_new)
		
		#Check if a new X_best has been found
		if f_new > f_best:
			print('A NEW X_BEST WAS FOUND')
			X_best = X_new
			f_best = f_new
			print('X_best',X_best)
			print('f_best',f_best)
			shutil.copy(path_best+'/streamflows_%d.csv'%i,'./CALIB_OUT')
			
			if os.path.exists('./CALIB_OUT/BEST_DOMAIN'):
				shutil.rmtree('./CALIB_OUT/BEST_DOMAIN')
				shutil.copytree(path_best+'/DOMAIN','./CALIB_OUT/BEST_DOMAIN')
				shutil.copy(path_best+'/CHANPARM.TBL','./CALIB_OUT/BEST_DOMAIN')
			else:
				shutil.copytree(path_best+'/DOMAIN','./CALIB_OUT/BEST_DOMAIN')
				shutil.copy(path_best+'/CHANPARM.TBL','./CALIB_OUT/BEST_DOMAIN')
				
			
		
		
		F_BEST_ALL.append(f_best)
		np.savetxt('./CALIB_OUT/F_BEST_ALL.csv',F_BEST_ALL,delimiter=',')
		np.savetxt('./CALIB_OUT/X_best_%03d.csv'%i,X_best,delimiter=',')
		
		
		
		plt.figure(1)
		plt.plot(F_BEST_ALL, color='purple')
		plt.ylim([0,4])
		plt.savefig('fitness.png',dpi=300)
		
		plot.plot_X_best()	
		plot.plot_streamflows()
			
		
		
