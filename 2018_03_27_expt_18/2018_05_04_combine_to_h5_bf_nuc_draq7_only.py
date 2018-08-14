import os
import sys
import vigra
import h5py
import re

if __name__ == "__main__":
    wellName = sys.argv[1]
    # well = os.path.basename(os.path.normpath(sourceDir))
    wellDir = sys.argv[2]
    sites = ['0000', '0001']
    # sites = ['0000']
    channels = ['1', '2', '5']
    scaledXResolution = 1280
    scaledYResolution = 1080
    os.environ['LD_LIBRARY_PATH'] = "$HOME/glibc-2.14/lib"

    for ste in sites:
        h5FilenameBase = os.path.join(wellDir, wellName + '_' + ste + '_' + 'c')
        h5ExampleFileName = h5FilenameBase + '2.h5'
        h5ExampleFile = vigra.impex.readHDF5(h5ExampleFileName, 'stacked_timepoints')
        data_type = h5ExampleFile.dtype
        #        print (h5File1.dtype)
        volume_shape = (3,) + h5ExampleFile.shape[::-1]
        #        print(volume_shape)
        axistags = vigra.defaultAxistags('ctyx')
        #        print (axistags)
        outputFilename = os.path.join(wellDir, wellName + '_' + ste + '_bf_nuc_draq7.h5')
        print('saving as ' + outputFilename)

        with h5py.File(outputFilename, 'w') as f:
            dset = f.create_dataset('data', shape=volume_shape, dtype=data_type, chunks=True)
            dset.attrs['axistags'] = axistags.toJSON()
            for counter, ch in enumerate(channels):
                h5FileName = h5FilenameBase + str(ch) + '.h5'
                print('now processing file ' + h5FileName)
                h5File = vigra.impex.readHDF5(h5FileName, 'stacked_timepoints')
                dset[counter-1, :, :, :] = h5File.transpose()

    print('reached end of 2018_03_29_bgsubtract_copy_combine.py for well ' + wellDir)