import os
import sys
import pandas as pd
import numpy as np

# potential init vars: folder_list, dflist, buffer, axon
# seems like experiment_dir is the object class
# no trailing slashes in user-specified paths? 

def filetiffs(experiment_dir):
	# take background subtracted tiffs in experiment_dir/tiff and sorts them into folders for KymoClear
	for item in sorted(os.listdir(experiment_dir+'/tiff')):
		os.makedirs(experiment_dir+'/tiff/'+item[0:3])
		os.rename(experiment_dir+'/tiff/'+item, experiment_dir+'/tiff/'+item[0:3]+'/'+item)

def sortkymos(experiment_dir): 
	# finds the kymographs in the experiment and packages them for submission to KymoButler as input
	os.makedirs(experiment_dir+'/4KymoButler')
	for field in sorted(os.listdir(experiment_dir+'/tiff/')):
		for fiber in sorted(os.listdir(experiment_dir+'/tiff/'+field+'/kymograph/')):
			if fiber.startswith('kymograph'):
				# now go in that directory fiber and take out the kymograph.tif, and rename it
				print ('renaming '+experiment_dir+'/tiff/'+field+'/kymograph/'+fiber+'/kymograph'+fiber[-1]+'.tif'+' to '
					+experiment_dir+'/4KymoButler/'+field+fiber[-1]+'.tif')
				os.rename(
					experiment_dir+'/tiff/'+field+'/kymograph/'+fiber+'/kymograph'+fiber[-1]+'.tif', 
					experiment_dir+'/4KymoButler/'+field+fiber[-1]+'.tif'
					)

def sortkbcsv(experiment_dir, kboutput_dir): 
	# renames KymoButler CSV output from the 'kboutput_dir' and sorts into appropriate subdirectories within 'experiment_dir/Results'
	# requires the kymographs to be present in a '4KymoButler' folder in 'experiment_dir'
	folder_list = ['f2fvelocities','pausetimes','raw','sortedVelocities','summary','trackCoordinates']
	sent=sorted(os.listdir(experiment_dir+'/4KymoButler')) # (ensure no zip file)
	for item in folder_list:
		os.makedirs(experiment_dir+'/Results/'+item) #create folders
		for entry in os.listdir(kboutput_dir):
			if entry.startswith(item):
				num = ''
				for ch in entry[2:]:
					if ch.isdigit():
						num = num +ch
				print('renaming '+kboutput_dir+'/'+entry+' to '+experiment_dir+'/Results/'+item+'/'+sent[int(num)-1][0:4]+entry[-4:])
				os.rename(kboutput_dir+'/'+entry, experiment_dir+'/Results/'+item+'/'+sent[int(num)-1][0:4]+entry[-4:]) 

def summaryframe(experiment_dir, dict_a, dict_b, culture='000000'):
	# requires 'summary' named files from 'sortkbcsv' to be in the appropriate 'Results' directory
	# requires two dictionaries that translate file designations (a,b,c...) to experimental conditions
	# returns a dataframe with particles labeled by treatment, field of view, axon number, experiment type, and 'culture' label from user input
	# also returns a dataframe of flux measurements
	# currently, this numbers axons from 1 to N, PER CONDITION, converting from the existing format of axons per FOV. 
	dflist = []
	fluxlist = []
	buffer='a'
	axon=0
	for item in sorted(os.listdir(experiment_dir+'/Results/summary/')):
		df = pd.read_csv(experiment_dir+'/Results/summary/'+item, index_col=0, header=1)
		flux = pd.read_csv(experiment_dir+'/Results/summary/'+item, index_col=None, header=None, usecols=[5,6], 
			names=['positive flux','negative flux'], skiprows=lambda x:x>0)
		df['var_A'] = dict_a[item[0]]
		df['var_B'] = dict_b[item[0]]
		df['FOV'] = int(item[1])
		df['experiment'] = item[2]
		df['culture'] = culture
		flux['var_A'] = dict_a[item[0]]
		flux['var_B'] = dict_b[item[0]]
		flux['FOV'] = int(item[1])
		flux['experiment'] = item[2]
		flux['culture'] = culture
		if item[0]==buffer:
			# first treatment condition; label axons starting at 1
			axon = axon+1
			df['axon'] = axon
			flux['axon'] = axon
		else:
			# new treatment condition, begin numbering axons at 1 again
			axon = 1
			df['axon'] = axon
			flux['axon'] = axon
			buffer = item[0]
		# determining flux by number spit out of kymobutler CONVERTING TO PER MINUTE
		flux.iloc[0,0] = float(flux.iloc[0,0].split('= ')[1]) * 60
		flux.iloc[0,1] = float(flux.iloc[0,1].split('= ')[1]) * 60
		# determining flux by counting number of vesicles in each condition
		#flux.iloc[0,0] = np.count_nonzero(df['Direction (1:Positive, 0:near-zero, -1:negative)'] == 1)
		#flux.iloc[0,1] = np.count_nonzero(df['Direction (1:Positive, 0:near-zero, -1:negative)'] == -1)
		dflist.append(df)
		fluxlist.append(flux)
	df = pd.concat(dflist, ignore_index=True)
	flux = pd.concat(fluxlist, ignore_index=True)
	return df,flux 



