import numpy as np
import os
import shutil
from netCDF4 import Dataset


def CHANupdate(BaseDir,RunDir,paramNames,f):
	BaseFilePath = os.path.join(BaseDir,'CHANPARM.TBL')
	AdjusFilePath = os.path.join(RunDir,'CHANPARM.TBL')
	
	
	shutil.copy(BaseFilePath,RunDir)
	
	BaseTbl= open(BaseFilePath,'r')
	AdjusTbl = open(AdjusFilePath,'w')
	LineNumber = 1
	for line in BaseTbl:
		if LineNumber<4:
			AdjusTbl.write(line)
		else:
			AdjusLine = line
			lineSplit = AdjusLine.split(',')
			if "Bw" in paramNames:
				bwValue = float(lineSplit[1])*float(f.adjusted[f['parameter'] == 'Bw'])				
			else:
				bwValue = float(lineSplit[1])
			if "HLINK" in paramNames:
				hlinkValue = float(lineSplit[2])*float(f.adjusted[f['parameter'] == 'HLINK'])
			else:
				hlinkValue = float(lineSplit[2])
			if "ChSSlp" in paramNames:
				chsslpValue = float(lineSplit[3])*float(f.adjusted[f['parameter'] == 'ChSSlp'])
			else:
				chsslpValue = float(lineSplit[3])
			if "MannN" in paramNames:
				mannValue = float(lineSplit[4])*float(f.adjusted[f['parameter'] == 'MannN'])
			else:
				mannValue = float(lineSplit[4])
			outStr = lineSplit[0] + ", " + str(bwValue) + ", " + str(hlinkValue) + \
                         ", " + str(chsslpValue) + ", " + str(mannValue) + "\n"
			AdjusTbl.write(outStr)
		LineNumber+=1
	
def NcFilesUpdate(BaseDir,RunDir,paramNames,f):
    # Compose input file paths.
    fullDomOrig = BaseDir + "/Fulldom.nc"
    hydroOrig = BaseDir + "/HYDRO_TBL_2D.nc"
    soilOrig = BaseDir + "/soil_properties.nc"
    gwOrig = BaseDir + "/GWBUCKPARM.nc"

    
    # Compose output file paths.
    fullDomOut = RunDir + "/DOMAIN/Fulldom.nc"
    hydroOut = RunDir + "/DOMAIN//HYDRO_TBL_2D.nc"
    soilOut = RunDir + "/DOMAIN//soil_properties.nc"
    gwOut = RunDir + '/DOMAIN//GWBUCKPARM.nc'	
	
    shutil.copy(fullDomOrig,fullDomOut)
    shutil.copy(hydroOrig,hydroOut)
    shutil.copy(soilOrig,soilOut)
    shutil.copy(gwOrig,gwOut)	

    # Open NetCDF parameter files for adjustment.
    idFullDom = Dataset(fullDomOut,'a')
    idSoil2D = Dataset(soilOut,'a')
    idGw = Dataset(gwOut,'a')
    idHydroTbl = Dataset(hydroOut,'a')	

    # Loop through and adjust each parameter accordingly.
    for param in paramNames:
        if param == "bexp":
            idSoil2D.variables['bexp'][:,:,:,:] = idSoil2D.variables['bexp'][:,:,:,:]*float(f.adjusted[f['parameter'] == 'bexp'])
        
        if param == "smcmax":
            idSoil2D.variables['smcmax'][:,:,:,:] = idSoil2D.variables['smcmax'][:,:,:,:]*float(f.adjusted[f['parameter'] == 'smcmax'])
        
        if param == "slope":
            idSoil2D.variables['slope'][:,:,:] = float(f.adjusted[f['parameter'] == 'slope'])
			
        if param == "lksatfac":
            idFullDom.variables['LKSATFAC'][:,:] = float(f.adjusted[f['parameter'] == 'lksatfac'])
        
        if param == "zmax":
            idGw.variables['Zmax'][:] = float(f.adjusted[f['parameter'] == 'zmax'])
        
        if param == "expon":
            idGw.variables['Expon'][:] = float(f.adjusted[f['parameter'] == 'expon'])
        
        if param == "cwpvt":
            idSoil2D.variables['cwpvt'][:,:,:] = idSoil2D.variables['cwpvt'][:,:,:]*float(f.adjusted[f['parameter'] == 'cwpvt'])
        
        if param == "vcmx25":
            idSoil2D.variables['vcmx25'][:,:,:] = idSoil2D.variables['vcmx25'][:,:,:]*float(f.adjusted[f['parameter'] == 'vcmx25'])
        
        if param == "mp":
            idSoil2D.variables['mp'][:,:,:] = idSoil2D.variables['mp'][:,:,:]*float(f.adjusted[f['parameter'] == 'mp'])
        
        if param == "hvt":
            idSoil2D.variables['hvt'][:,:,:] = idSoil2D.variables['hvt'][:,:,:]*float(f.adjusted[f['parameter'] == 'hvt'])
        
        if param == "mfsno":
            idSoil2D.variables['mfsno'][:,:,:] = idSoil2D.variables['mfsno'][:,:,:]*float(f.adjusted[f['parameter'] == 'mfsno'])
        
        if param == "refkdt":
            idSoil2D.variables['refkdt'][:,:,:] = float(f.adjusted[f['parameter'] == 'refkdt'])
        
        if param == "dksat":
            idSoil2D.variables['dksat'][:,:,:,:] = idSoil2D.variables['dksat'][:,:,:,:]*float(f.adjusted[f['parameter'] == 'dksat'])
        
        if param == "retdeprtfac":
            idFullDom.variables['RETDEPRTFAC'][:,:] = float(f.adjusted[f['parameter'] == 'retdeprtfac'])
        
        if param == "ovroughrtfac":
            idFullDom.variables['OVROUGHRTFAC'][:,:] = float(f.adjusted[f['parameter'] == 'ovroughrtfac'])
            
        if param == "dksat":
            idHydroTbl.variables['LKSAT'][:,:] = idHydroTbl.variables['LKSAT'][:,:]*float(f.adjusted[f['parameter'] == 'dksat'])
            
        if param == "smcmax":
            idHydroTbl.variables['SMCMAX1'][:,:] = idHydroTbl.variables['SMCMAX1'][:,:]*float(f.adjusted[f['parameter'] == 'smcmax'])
            
        if param == "rsurfexp":
            idSoil2D.variables['rsurfexp'][:,:,:] = float(f.adjusted[f['parameter'] == 'rsurfexp'])
        
            
    # Close NetCDF files
    idFullDom.close()
    idSoil2D.close()
    idGw.close()
    idHydroTbl.close()	