# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 14:54:46 2017

@author: jchang6
"""
""" 
This script goes into each subdirectory, identifies the relevant pairs of h5 files, load them up, and save them with appropriate axis tags in a new .h5 file.

"""
# import vigra
# import h5py
import os
import re


def writeCombineh5Script(subDir, codeDirectory):
    outputString=r"""import vigra
import h5py
import os
import re

#    First, figure out what the well and sequence #, and site number are. Set up a regular expression and capture the groups. Note that this script assumes that there are three digits in the time.

if __name__ == "__main__":
    previousDirectory = os.getcwd()
    print('Now processing directory '+'{sbdr}')
    os.chdir('{sbdr}')
    
    pattern = re.compile(r'Well([A-Z]\d\d)_(\d\d\d\d)c([0-9])_t20_to_tend.h5') 
    allFiles = os.listdir('{sbdr}')
    well = list(set([pattern.match(f).group(1) for f in allFiles if pattern.match(f)]))
    sites = sorted(set([pattern.match(f).group(2) for f in allFiles if pattern.match(f)]))
    channels = sorted(set([pattern.match(f).group(3) for f in allFiles if pattern.match(f)]))    
    
       
    print('This directory contains images from well '+ str(well[0])+ ' and has channels ' + str(channels))
    
    
    
    for ste in sites:
        h5Filename1 = os.path.join('{sbdr}', 'Well'+well[0]+'_'+ste+'c1_t20_to_tend.h5')
        h5Filename2 = os.path.join('{sbdr}', 'Well'+well[0]+'_'+ste+'c2_t20_to_tend.h5')
        if len(channels) == 3:
            h5Filename3 = os.path.join('{sbdr}', 'Well'+well[0]+'_'+ste+'c3_t20_to_tend.h5')
        elif len(channels) == 4:
            h5Filename3 = os.path.join('{sbdr}', 'Well'+well[0]+'_'+ste+'c4_t20_to_tend.h5')
        elif len(channels) == 5:
            h5Filename3 = os.path.join('{sbdr}', 'Well'+well[0]+'_'+ste+'c5_t20_to_tend.h5')
        print('now processing files '+ h5Filename1 + ' and ' + h5Filename2 + ' and ' + h5Filename3)
    
        h5File1 = vigra.impex.readHDF5(h5Filename1, 'stacked_timepoints')
        h5File2 = vigra.impex.readHDF5(h5Filename2, 'stacked_timepoints')
        h5File3 = vigra.impex.readHDF5(h5Filename3, 'stacked_timepoints')
        
        data_type = h5File1.dtype
    #        print (h5File1.dtype)
        volume_shape = (3,) + h5File1.shape[::-1]
    #        print(volume_shape)
        axistags = vigra.defaultAxistags('ctyx')
    #        print (axistags)
        
        outputFilename = os.path.join('{sbdr}', 'Well'+well[0]+'_'+ste+'_bf_nuc_nucview_t20_to_tend.h5')
        print('saving as ' + outputFilename)
        with h5py.File(outputFilename, 'w') as f:
            dset = f.create_dataset('data', shape=volume_shape, dtype=data_type, chunks=True)
            dset.attrs['axistags'] = axistags.toJSON()
            dset[0,:,:,:]=h5File1.transpose()
            dset[1,:,:,:]=h5File2.transpose()
            dset[2,:,:,:]=h5File3.transpose()
    os.chdir(previousDirectory)""".format(sbdr=str(subDir))
    # print(outputString.format(sbdr=subDir))
    # print(subDir)
    with open(os.path.join(codeDirectory,'combine_c1_c2_script_' + os.path.basename(os.path.normpath(subDir))+ '_t20_to_tend.py'), 'w') as f:
        f.write(outputString)



if __name__ == "__main__":
    #specify parent directory containing wells. Code assumes that it includes backslashes at the end.
    directory = '/awlab/users/jchang/raw_data/2017_11_10_expt_15_SK_dose_response_h5'
    codeDirectoryInput = '/awlab/users/jchang/code/2017_11_10_expt_15'
    codeDirectory = os.path.join(codeDirectoryInput, 'temp_scripts')
    if not os.path.exists(codeDirectory):
        os.makedirs(codeDirectory)
    print('this script will produce a set of python scripts, each of which processes one well, and a shell script to run that set of python scripts.')
    print('parent source directory to process: {}'.format(directory))
    print('code directory (where the scripts will be written): {}'.format(codeDirectory))


    wellRegExp = re.compile('[A-H]\d\d')
    subDirectories = sorted([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)) & bool(wellRegExp.match(name))])
    master_script_path = os.path.join(codeDirectory, 'combine_bf_nuc_nucview_t20_to_tend_master_script')
    print('all subdirectories: {}'.format(subDirectories))
    print('master script path: {}'.format(master_script_path))
    for counter, subDir in enumerate(subDirectories):
        print('writing script for directory ' + subDir)
        subDirectory = os.path.join(directory, subDir)
        writeCombineh5Script(subDirectory, codeDirectory)
        line_to_write=r'source activate py35 && export LD_LIBRARY_PATH=$HOME/glibc-2.14/lib && python ' + os.path.join(codeDirectory,'combine_c1_c2_script_' + os.path.basename(os.path.normpath(subDir))+ '_t20_to_tend.py') + ' && source deactivate\n'
        if counter == 0:
            f = open(master_script_path, 'w')
            f.write(line_to_write)
        else:
            with open(master_script_path, 'a+') as f:
                f.write(line_to_write)