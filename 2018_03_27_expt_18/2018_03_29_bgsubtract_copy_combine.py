import os
import sys
import vigra
import h5py

if __name__ == "__main__":
    wellName = sys.argv[1]
    # well = os.path.basename(os.path.normpath(sourceDir))
    wellDir = sys.argv[2]
    print('Now processing directory {}'.format(wellDir))
    print('starting ImageJ...')
    os.environ['LD_LIBRARY_PATH'] = ""
    os.system(
        '{fijiLocation} --allow-multiple --headless --console --plugins ~ -macro {macroLocation}'.format(
            fijiLocation='/awlab/users/jchang/programs/Fiji.app/ImageJ-linux64', macroLocation=r'/awlab/users/jchang/programs/Fiji.app/macros/tempMacro_2018_03_27_' + wellName + '.ijm'))
    os.environ['LD_LIBRARY_PATH'] = '$HOME/glibc-2.14/lib'
    print('ImageJ finished on directory {}'.format(wellDir))
    os.environ['LD_LIBRARY_PATH'] = "$HOME/glibc-2.14/lib"

    os.chdir(wellDir)
    sites = ['0000', '0001']
    # sites = ['0000']
    channels = ['1', '2', '3', '4', '5']
    exampleFile = 'channel_5_site_0001_306.tif'

    info = vigra.impex.ImageInfo(exampleFile)
    X, Y, _chan = info.getShape()
    T = 307
    times = list(range(0,T))
    dtype = info.getDtype()
    volume_shape = (T, Y, X)
    axistags = vigra.defaultAxistags('tyx')

    #    print('previousDirectory = {}'.format(previousDirectory))
    #    print('sourceDir = {}'.format(sourceDir))
    #    print('targetDir = {}'.format(targetDir))
    print('file details: {}'.format((X, Y, T, dtype)))

    for ste in sites:
        for ch in channels:
            h5Path = os.path.join(wellDir, wellName + '_' + ste + '_' + 'c' + ch + '.h5')
            print('now saving file ' + h5Path)
            with h5py.File(h5Path, 'w') as f:
                dset = f.create_dataset('stacked_timepoints', shape=volume_shape, dtype=dtype, chunks=True)
                dset.attrs['axistags'] = axistags.toJSON()
                for counter, time in enumerate(times):
                    currFile = 'channel_' + ch + '_site_' + ste + '_' + "{0:0>3}".format(time) + '.tif'
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
                            print(currFileInfo)
                            img = vigra.impex.readImage(currFile, dtype='NATIVE')
                            #                        print('skipped')
                            dset[counter, :, :] = img.transpose()
                            # print('deleting background-subtracted tif')
                            # os.remove(currFile)
                        else:
                            print(
                                'resolution does not match resolution of exampleFile, keeping background-subtracted tif')



    for ste in sites:
        h5FilenameBase = os.path.join(wellDir, wellName + '_' + ste + '_' + 'c')
        h5ExampleFileName = h5FilenameBase + '2.h5'
        h5ExampleFile = vigra.impex.readHDF5(h5ExampleFileName, 'stacked_timepoints')
        data_type = h5ExampleFile.dtype
        #        print (h5File1.dtype)
        volume_shape = (5,) + h5ExampleFile.shape[::-1]
        #        print(volume_shape)
        axistags = vigra.defaultAxistags('ctyx')
        #        print (axistags)
        outputFilename = os.path.join(wellDir, wellName + '_' + ste + '.h5')
        print('saving as ' + outputFilename)

        with h5py.File(outputFilename, 'w') as f:
            dset = f.create_dataset('data', shape=volume_shape, dtype=data_type, chunks=True)
            dset.attrs['axistags'] = axistags.toJSON()
            for ch in channels:
                h5FileName = h5FilenameBase + str(ch) + '.h5'
                print('now processing file ' + h5FileName)
                h5File = vigra.impex.readHDF5(h5FileName, 'stacked_timepoints')
                dset[(int(ch)-1), :, :, :] = h5File.transpose()

    print('reached end of 2018_03_29_bgsubtract_copy_combine.py for well ' + wellDir)