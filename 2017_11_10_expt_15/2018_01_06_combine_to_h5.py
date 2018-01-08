import vigra
import h5py
import os
import re

#    First, figure out what the well and sequence #, and site number are. Set up a regular expression and capture the groups. Note that this script assumes that there are three digits in the time.

if __name__ == "__main__":
    sourceDir = sys.argv[1]
    tStart = int(sys.argv[2])
    if sys.argv[3] == ':':
        tEnd = 'end'
    else:
        tEnd = int(sys.argv[3])

    previousDirectory = os.getcwd()
    print('combining .tifs to .h5 in directory ' + sourceDir + ' for times ' + str(tStart) + ' through ' + str(tEnd))

    os.chdir(sourceDir)

    pattern = re.compile(r'Well([A-Z]\d\d)_Seq(\d+)t(\d+)[A-Z]\d\d_(\d+)c([0-9]).tif')
    allFiles = os.listdir(sourceDir)
    well = list(set([pattern.match(f).group(1) for f in allFiles if pattern.match(f)]))
    sequence = list(set([pattern.match(f).group(2) for f in allFiles if pattern.match(f)]))
    times = sorted(set([pattern.match(f).group(3) for f in allFiles if pattern.match(f)]))
    sites = sorted(set([pattern.match(f).group(4) for f in allFiles if pattern.match(f)]))
    channels = sorted(set([pattern.match(f).group(5) for f in allFiles if pattern.match(f)]))

    exampleFile = 'Well' + well[-1] + '_Seq' + sequence[-1] + 't' + times[-1] + well[-1] + '_' + sites[-1] + 'c' + \
                  channels[-1] + '.tif'
    info = vigra.impex.ImageInfo(exampleFile)
    X, Y, _chan = info.getShape()
    if tEnd=='end':
        times=times[tStart:]
    else:
        times=times[tStart:tEnd]
    T = int(len(times))
    dtype = info.getDtype()
    volume_shape = (T, Y, X)
    axistags = vigra.defaultAxistags('tyx')

    #    print('previousDirectory = {}'.format(previousDirectory))
    #    print('sourceDir = {}'.format(sourceDir))
    #    print('targetDir = {}'.format(targetDir))
    print('well = {}'.format(well))
    print('sequence = {}'.format(sequence))
    print('exampleFile = {}'.format(exampleFile))
    print('file details: {}'.format((X, Y, T, dtype)))

    for ste in sites:
        for ch in channels:
            h5Path = os.path.join(sourceDir, 'Well' + well[0] + '_' + ste + 'c' + ch + '_t'+str(tStart+1)+'_to_t'+str(tEnd)+'.h5')
            print('now saving file ' + h5Path)
            with h5py.File(h5Path, 'w') as f:
                dset = f.create_dataset('stacked_timepoints', shape=volume_shape, dtype=dtype, chunks=True)
                dset.attrs['axistags'] = axistags.toJSON()
                for counter, time in enumerate(times):
                    currFile = 'Well' + well[0] + '_Seq' + sequence[0] + 't' + time + well[
                        0] + '_' + ste + 'c' + ch + '.tif'
                    print('trying to save ' + currFile)
                    #                    print(time)
                    #                    print(ch)
                    #                    print(T)
                    #                    print(volume_shape)
                    #                    print(times)
                    if os.path.isfile(currFile):
                        currFileInfo = vigra.impex.ImageInfo(currFile)
                        currX, currY, _currChan = currFileInfo.getShape()
                        if currX == X and currY == Y:
                            print('resolution matches resolution of exampleFile, now reading and saving')
                            img = vigra.impex.readImage(currFile, dtype='NATIVE')
                            #                        print('skipped')
                            dset[counter, :, :] = img.transpose()
                            # print('deleting background-subtracted tif')
                            # os.remove(currFile)
                        else:
                            print(
                                'resolution does not match resolution of exampleFile, keeping background-subtracted tif')
    os.chdir(previousDirectory)




    # subDir = sys.argv[1]
    #
    # previousDirectory = os.getcwd()
    # print('Now processing directory ' + subDir)
    # os.chdir(subDir)
    #
    # pattern = re.compile(r'Well([A-Z]\d\d)_(\d\d\d\d)c([0-9]).h5')
    # allFiles = os.listdir(subDir)
    # well = list(set([pattern.match(f).group(1) for f in allFiles if pattern.match(f)]))
    # sites = sorted(set([pattern.match(f).group(2) for f in allFiles if pattern.match(f)]))
    #
    # print('This directory contains images from well: ' + str(well[0]))
    #
    # for ste in sites:
    #     h5Filename1 = os.path.join(subDir, 'Well' + well[0] + '_' + ste + 'c1.h5')
    #     h5Filename2 = os.path.join(subDir, 'Well' + well[0] + '_' + ste + 'c2.h5')
    #     print('now processing files ' + h5Filename1 + ' and ' + h5Filename2)
    #
    #     h5File1 = vigra.impex.readHDF5(h5Filename1, 'stacked_timepoints')
    #     h5File2 = vigra.impex.readHDF5(h5Filename2, 'stacked_timepoints')
    #
    #     data_type = h5File1.dtype
    #     #        print (h5File1.dtype)
    #     volume_shape = h5File1.shape + (2,)
    #     #        print(volume_shape)
    #     axistags = vigra.defaultAxistags('xytc')
    #     #        print (axistags)
    #
    #     outputFilename = os.path.join(subDir, 'Well' + well[0] + '_' + ste + 'c1-2.h5')
    #     print('saving as ' + outputFilename)
    #     with h5py.File(outputFilename, 'w') as f:
    #         dset = f.create_dataset('data', shape=volume_shape, dtype=data_type, chunks=True)
    #         dset.attrs['axistags'] = axistags.toJSON()
    #         dset[:, :, :, 0] = h5File1
    #         dset[:, :, :, 1] = h5File2
    # os.chdir(previousDirectory)