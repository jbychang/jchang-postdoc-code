import vigra
import h5py
import os
import re

#    First, figure out what the well and sequence #, and site number are. Set up a regular expression and capture the groups. Note that this script assumes that there are three digits in the time.

if __name__ == "__main__":
    previousDirectory = os.getcwd()
    print('Now processing directory '+'/awlab/users/jchang/raw_data/2017_11_10_expt_15_SK_dose_response_h5/G02')
    os.chdir('/awlab/users/jchang/raw_data/2017_11_10_expt_15_SK_dose_response_h5/G02')
    
    pattern = re.compile(r'Well([A-Z]\d\d)_(\d\d\d\d)c([0-9])_t1_to_t19.h5') 
    allFiles = os.listdir('/awlab/users/jchang/raw_data/2017_11_10_expt_15_SK_dose_response_h5/G02')
    well = list(set([pattern.match(f).group(1) for f in allFiles if pattern.match(f)]))
    sites = sorted(set([pattern.match(f).group(2) for f in allFiles if pattern.match(f)]))
        
    
       
    print('This directory contains images from well: '+ str(well[0]))
    
    
    
    for ste in sites:
        h5Filename1 = os.path.join('/awlab/users/jchang/raw_data/2017_11_10_expt_15_SK_dose_response_h5/G02', 'Well'+well[0]+'_'+ste+'c1_t1_to_t19.h5')
        h5Filename2 = os.path.join('/awlab/users/jchang/raw_data/2017_11_10_expt_15_SK_dose_response_h5/G02', 'Well'+well[0]+'_'+ste+'c2_t1_to_t19.h5')
        print('now processing files '+ h5Filename1 + ' and ' + h5Filename2)
    
        h5File1 = vigra.impex.readHDF5(h5Filename1, 'stacked_timepoints')
        h5File2 = vigra.impex.readHDF5(h5Filename2, 'stacked_timepoints')
    
        data_type = h5File1.dtype
    #        print (h5File1.dtype)
        volume_shape = h5File1.shape+(2,)
    #        print(volume_shape)
        axistags = vigra.defaultAxistags('xytc')
    #        print (axistags)
        
        outputFilename = os.path.join('/awlab/users/jchang/raw_data/2017_11_10_expt_15_SK_dose_response_h5/G02', 'Well'+well[0]+'_'+ste+'c1-2_t1_to_t19.h5')
        print('saving as ' + outputFilename)
        with h5py.File(outputFilename, 'w') as f:
            dset = f.create_dataset('data', shape=volume_shape, dtype=data_type, chunks=True)
            dset.attrs['axistags'] = axistags.toJSON()
            dset[:,:,:,0]=h5File1
            dset[:,:,:,1]=h5File2
    os.chdir(previousDirectory)