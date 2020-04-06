import numpy as np
import os
import matplotlib.pyplot as plt


def plot_X_best():
	fig = plt.subplots(squeeze=False)
	ax_refkdt      = plt.subplot2grid((5, 4), (0, 0))
	ax_slope       = plt.subplot2grid((5, 4), (0, 1))
	ax_retdeprtfac = plt.subplot2grid((5, 4), (0, 2))
	ax_lksatfac    = plt.subplot2grid((5, 4), (0, 3))

	ax_bexp = plt.subplot2grid((5, 4), (1, 0))
	ax_smcmax = plt.subplot2grid((5, 4), (1, 1))
	ax_dksat = plt.subplot2grid((5, 4), (1, 2))

	ax_cwpvt = plt.subplot2grid((5, 4), (2, 0))
	ax_vcmx25 = plt.subplot2grid((5, 4), (2, 1))
	ax_mp = plt.subplot2grid((5, 4), (2, 2))

	ax_zmax = plt.subplot2grid((5, 4), (3, 0))
	ax_expon = plt.subplot2grid((5, 4), (3, 1))

	ax_Bw = plt.subplot2grid((5, 4), (4, 0))
	ax_MannN = plt.subplot2grid((5, 4), (4, 1))

	ax_refkdt.set_ylabel('Runoff parameters')
	ax_bexp.set_ylabel('Soil parameters')
	ax_cwpvt.set_ylabel('Vegetation parameters')
	ax_zmax.set_ylabel('Groundwater parameters')
	ax_Bw.set_ylabel('Channel parameters')



	ax_bexp.set_title('bexp')
	ax_smcmax.set_title('smcmax')
	ax_dksat.set_title('dksat')
	ax_refkdt.set_title('refkdt')
	ax_slope.set_title('slope')
	ax_retdeprtfac.set_title('retdeprtfac')
	ax_lksatfac.set_title('lksatfac')
	ax_zmax.set_title('zmax')
	ax_expon.set_title('expon')
	ax_cwpvt.set_title('cwpvt')
	ax_vcmx25.set_title('vcmx25')
	ax_mp.set_title('mp')
	ax_Bw.set_title('Bw')
	ax_MannN.set_title('MannN')



	files = os.listdir('./CALIB_OUT')
	files = [x for x in files if x.startswith('X_best')]
	files = sorted(files)

	X = np.empty((14,0),dtype=float)
	for file in files:
		X_file = np.genfromtxt('./CALIB_OUT/'+file,delimiter=',').reshape(14,1)
		X = np.append(X,X_file,axis=1)
	
	ax_bexp.plot(X[0,:],'*')
	ax_smcmax.plot(X[1,:],'*')
	ax_dksat.plot(X[2,:],'*')
	ax_refkdt.plot(X[3,:],'*')
	ax_slope.plot(X[4,:],'*')
	ax_retdeprtfac.plot(X[5,:],'*')
	ax_lksatfac.plot(X[6,:],'*')
	ax_zmax.plot(X[7,:],'*')
	ax_expon.plot(X[8,:],'*')
	ax_cwpvt.plot(X[9,:],'*')
	ax_vcmx25.plot(X[10,:],'*')
	ax_mp.plot(X[11,:],'*')
	ax_Bw.plot(X[12,:],'*')
	ax_MannN.plot(X[13,:],'*')


	fig = plt.gcf()
	fig.subplots_adjust(wspace=0.5)
	fig.subplots_adjust(hspace=0.4)
	fig.set_size_inches(12, 12) #width, Height
	fig.savefig('./CALIB_OUT/plots/X_bests.png',dpi=300)

def plot_streamflows():
	obs_data = np.genfromtxt('OBS_data.csv',delimiter=',')
	
	fig, axes = plt.subplots(2, 2)

	axes[0,0].set_title('station 0 E 8071280')
	axes[0,1].set_title('station 1 D 8070200')
	axes[1,0].set_title('station 2 B 8071000')
	axes[1,1].set_title('station 3 C 8070500')


	files = os.listdir('./CALIB_OUT')
	files = [x for x in files if x.startswith('stream')]
	files = sorted(files)

	for file in files:
		stream_file = np.genfromtxt('./CALIB_OUT/'+file,delimiter=',')
		axes[0,0].semilogy(stream_file[:,1],'grey')
		axes[0,1].semilogy(stream_file[:,2],'grey')
		axes[1,0].semilogy(stream_file[:,3],'grey')
		axes[1,1].semilogy(stream_file[:,4],'grey')



	axes[0,0].semilogy(obs_data[:,1],'k')
	axes[0,1].semilogy(obs_data[:,2],'k')
	axes[1,0].semilogy(obs_data[:,3],'k')
	axes[1,1].semilogy(obs_data[:,4],'k')
	
	fig.set_size_inches(24, 12) #width, Height
	fig.savefig('./CALIB_OUT/plots/streamflows.png',dpi=300)