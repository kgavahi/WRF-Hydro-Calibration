import numpy as np
from read_CHANOBS import read_CHANOBS

def CORREL(X,Y):
	X_bar = np.nanmean(X)
	Y_bar = np.nanmean(Y)
	numerator = np.nansum((X - X_bar) * (Y - Y_bar))
	denominator = np.nansum((X - X_bar)**2)**0.5 * np.nansum((Y - Y_bar)**2)**0.5
	r = numerator / denominator	
	return r
def KGE(x,y):
	r = CORREL(x,y)
	t1 = (r-1)**2
	t2 = (np.nanstd(x)/np.nanstd(y)-1)**2
	t3 = (np.nanmean(x)/np.nanmean(y)-1)**2
	return 1 - (t1+t2+t3)**0.5

def fitness(path):
	streamflows = read_CHANOBS(path)
	OBS_data = np.genfromtxt('OBS_data.csv',delimiter=',')
	kge = 0
	for i in range(1,5):
		x = streamflows[:,i]
		y = OBS_data[:,i]	
		kge_st = KGE(x,y)
		print('kge of st',i,kge_st)
		kge+=kge_st
	return kge