# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 14:54:46 2017

@author: jchang6
"""

""" 
This script goes into each subdirectory, identify the relevant pairs of h5 files, load them up, and save them with appropriate axis tags in a new .h5 file.

"""
import vigra
import h5py
import os
import re


def combineh5(subDirectory):
#    First, figure out what the well and sequence #, and site number are. Set up a regular expression and capture the groups. Note that this script assumes that there are three digits in the time.
    previousDirectory = os.getcwd()
    print('Now processing directory '+subDirectory)
    os.chdir(subDirectory)
    
    pattern = re.compile(r'Well([A-Z]\d\d)_(\d\d\d\d)c([0-9]).h5') 
    allFiles = os.listdir(subDirectory)
    well = list(set([pattern.match(f).group(1) for f in allFiles if pattern.match(f)]))
    sites = sorted(set([pattern.match(f).group(2) for f in allFiles if pattern.match(f)]))
    

   
    print('This directory contains images from well: {}'.format(well[0]))


    
    for ste in sites:
        h5Filename1 = os.path.join(subDirectory, 'Well'+well[0]+'_'+ste+'c1.h5')
        h5Filename2 = os.path.join(subDirectory, 'Well'+well[0]+'_'+ste+'c2.h5')
        print('now processing files '+ h5Filename1 + ' and ' + h5Filename2)

        h5File1 = vigra.impex.readHDF5(h5Filename1, 'stacked_timepoints')
        h5File2 = vigra.impex.readHDF5(h5Filename2, 'stacked_timepoints')

        data_type = h5File1.dtype
#        print (h5File1.dtype)
        volume_shape = h5File1.shape+(2,)
#        print(volume_shape)
        axistags = vigra.defaultAxistags('xytc')
#        print (axistags)
        
        outputFilename = os.path.join(subDirectory, 'Well'+well[0]+'_'+ste+'c1-2.h5')
        print('saving as ' + outputFilename)
        with h5py.File(outputFilename, 'w') as f:
            dset = f.create_dataset('data', shape=volume_shape, dtype=data_type, chunks=True)
            dset.attrs['axistags'] = axistags.toJSON()
            dset[:,:,:,0]=h5File1
            dset[:,:,:,1]=h5File2
            
        
    os.chdir(previousDirectory)
    return

if __name__ == "__main__":
    #specify parent directory containing wells. Code assumes that it includes backslashes at the end.
    directory = '/awlab/users/jchang/raw_data/2017_11_10_expt_15_SK_dose_response_h5'
    print('parent source directory to process: {}'.format(directory))
   

    wellRegExp = re.compile('[A-H]\d\d')
    subDirectories = sorted([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)) & bool(wellRegExp.match(name))])
    print('all subdirectories: {}'.format(subDirectories))
    for subDir in subDirectories[0:30]:
        subDirectory = os.path.join(directory, subDir)
        combineh5(subDirectory)