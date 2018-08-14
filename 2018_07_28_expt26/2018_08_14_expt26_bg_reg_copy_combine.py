import os
import sys
import vigra
import h5py
import re



# In this experiment, I have three chunks of time courses: 


if __name__ == "__main__":
    wellName = sys.argv[1]
    # well = os.path.basename(os.path.normpath(sourceDir))
    wellDir = sys.argv[2]
    sites = ['0000', '0001']
    # sites = ['0000']
    channels = ['1', '2', '3', '4', '5']
    scaledXResolution = 1280
    scaledYResolution = 1080

# First, run ImageJ scripts to background subtract, scale, copy files to raw_data folder, and register (ch1) and transform (all other channels):
    print('Now processing directory {}'.format(wellDir))
    print('starting bg subtract and copy in ImageJ...')
    os.environ['LD_LIBRARY_PATH'] = ""
    command = '{fijiLocation} --allow-multiple --headless --console -macro {macroLocation}'.format(
            fijiLocation='/awlab/users/jchang/programs/Fiji.app.latest/ImageJ-linux64', macroLocation=r'/awlab/users/jchang/programs/Fiji.app/macros/tempMacro_2018_03_27_' + wellName + '.ijm')
    os.system(command)
    print('ImageJ finished bg subtract and copy on directory {}'.format(wellDir))
    for ste in sites:
        print('Starting registration on well '+ wellDir + ' and site ' + ste + ' in ImageJ...')
        command = '{fijiLocation} --headless --run {scriptLocation}'.format(
                fijiLocation='/awlab/users/jchang/programs/Fiji.app.latest/ImageJ-linux64', scriptLocation=r'/awlab/users/jchang/programs/Fiji.app/macros/tempMacro_registration_2018_03_27_' + wellName + '_site_'+ ste + '.py')
        print('command: '+ command)
        os.system(command)
        print('Registration on well '+ wellDir + ' and site ' + ste + ' finished. Starting transforming in ImageJ...')
        command = '{fijiLocation} --allow-multiple --headless --console -macro {scriptLocation}'.format(
                fijiLocation='/awlab/users/jchang/programs/Fiji.app.latest/ImageJ-linux64',
                scriptLocation=r'/awlab/users/jchang/programs/Fiji.app/macros/tempMacro_transform_2018_03_27_' + wellName + '_site_' + ste + '.ijm')
        print('command: ' + command)
        os.system(command)
    print('ImageJ finished on well {}'.format(wellDir))

# Next, crop each image using ImageJ again:
    for ste in sites:
        transformsDir = os.path.join(wellDir, ste+'_transforms')
        fileNames = sorted(os.listdir(transformsDir))
        a = []
        b = []
        for counter, fn in enumerate(fileNames[1:]):
            with open(os.path.join(transformsDir,fn),'r') as f:
                text = f.read()
            pattern = re.compile(r'data="([\d\.E\-\+]+)\s+([\d\.E\-\+]+)"')
            matches = pattern.findall(text)
            # print(text)
            # print(matches)
            atemp = 0
            btemp = 0
            for match in matches:
                # print(match)
                # print(int(float(match[0])))
                # print(int(float(match[1])))
                atemp += round(float(match[0]))
                btemp += round(float(match[1]))
            a.append(atemp)
            b.append(btemp)
        # print(a)
        # print(b)
        # print(str(min(a)) + ' ' + str(min(b)))
        # print(str(max(a)) + ' ' + str(max(b)))
        xshift = max(a)-min(a)
        yshift = max(b)-min(b)
        print('x shift: ' + str(xshift))
        print('y shift: ' + str(yshift))
        macroText = r"""run("Image Sequence...", "open={imageDir} file=(.*{site}.*tif) sort");
makeRectangle({xShift}+10, {yShift}+10, 1280-{xShift}-20, 1080-{yShift}-20);
run("Crop");
run("Image Sequence... ", "format=TIFF name=[] digits=[] use save={imageDir}/channel_1_site_0000_000.tif");
            """.format(imageDir=wellDir, site=ste, xShift=xshift, yShift=yshift)
        macroFileName = r'/awlab/users/jchang/programs/Fiji.app/macros/tempMacro_2018_03_27_' + wellName + '_site_' + ste + '_crop.ijm'
        ijf = open(macroFileName, 'w')
        ijf.write(macroText)
        ijf.close()
        print('Starting cropping on well ' + wellDir + ' and site ' + ste + ' in ImageJ...')
        command = '{fijiLocation} --allow-multiple --headless --console -macro {macroLocation}'.format(
            fijiLocation='/awlab/users/jchang/programs/Fiji.app.latest/ImageJ-linux64',
            macroLocation=macroFileName)
        print('command: ' + command)
        os.system(command)
        print('Cropping on well ' + wellDir + ' and site ' + ste + ' finished.')

# Finally, combine to .h5
    os.environ['LD_LIBRARY_PATH'] = "$HOME/glibc-2.14/lib"
    os.chdir(wellDir)
    for ste in sites:
        exampleFile = 'channel_5_site_' + ste + '_306.tif'
        info = vigra.impex.ImageInfo(exampleFile)
        X, Y, _chan = info.getShape()
        T = 307
        times = list(range(0, T))
        dtype = info.getDtype()
        volume_shape = (T, Y, X)
        axistags = vigra.defaultAxistags('tyx')
        print('file details: {}'.format((X, Y, T, dtype)))
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