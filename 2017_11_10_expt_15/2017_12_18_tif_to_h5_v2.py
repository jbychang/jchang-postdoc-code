# -*- coding: utf-8 -*-
"""
This version of the macro takes all .tifs that don't contain "c1.tif" and does background subtraction on them all, saving them as "filename-bg.tif" in the target directory, then deletes all the .tifs in the target directory (since they will be saved as .h5). 
"""

import os
import re
import vigra
import h5py


def bgSubtractAndCopy(sourceDir, targetDir):
    macroText="""list = getFileList("{srcDir}");
	
    for (i=0; i<list.length; i++) {{
        print("ImageJ: processing file "+list[i] + ' in directory {srcDir}');
        print("ImageJ: this file is from channel 1: "+endsWith(list[i], "c1.tif"));
        if (endsWith(list[i], "c1.tif")) {{
           File.copy("{srcDir}"+File.separator + list[i],"{trgtDir}"+File.separator+list[i]);
		}}
        else {{
                print("{srcDir}"+File.separator + list[i]);
                open("{srcDir}"+File.separator + list[i]);
                run("Subtract Background...", "rolling=100");
            saveAs("Tiff", "{trgtDir}"+File.separator+list[i]);
        }}
     }}""".format(srcDir=sourceDir, trgtDir=targetDir)
        
    print('writing this ImageJ macro:\n'+macroText)
    print('writing macro to {}'.format(r'/awlab/users/jchang/programs/Fiji.app/macros/tempMacro.ijm'))
    f=open(r'/awlab/users/jchang/programs/Fiji.app/macros/tempMacro.ijm','w')
    f.write(macroText)
    f.close()
 
    print('starting ImageJ...')
    os.environ['LD_LIBRARY_PATH'] = ""
    os.system('{fijiLocation} --headless --console --plugins ~ -macro /awlab/users/jchang/programs/Fiji.app/macros/tempMacro.ijm'.format(fijiLocation='/awlab/users/jchang/programs/Fiji.app/ImageJ-linux64'))
    os.environ['LD_LIBRARY_PATH'] = '$HOME/glibc-2.14/lib'
    print('ImageJ finished')
    return
    
def processDirectory(sourceDir, targetDir):
#    First, figure out what the well and sequence #, and site number are. Set up a regular expression and capture the groups. Note that this script assumes that there are three digits in the time.
    previousDirectory = os.getcwd()
    print('processing sourceDir '+sourceDir+' and targetDir ' + targetDir)
    bgSubtractAndCopy(sourceDir, targetDir)
    
    os.chdir(targetDir)
    
    pattern = re.compile(r'Well([A-Z]\d\d)_Seq(\d+)t(\d+)[A-Z]\d\d_(\d+)c([0-9]).tif')
    allFiles = os.listdir(targetDir)
    well = list(set([pattern.match(f).group(1) for f in allFiles if pattern.match(f)]))
    sequence = list(set([pattern.match(f).group(2) for f in allFiles if pattern.match(f)]))
    times = sorted(set([pattern.match(f).group(3) for f in allFiles if pattern.match(f)]))
    sites = sorted(set([pattern.match(f).group(4) for f in allFiles if pattern.match(f)]))
    channels = sorted(set([pattern.match(f).group(5) for f in allFiles if pattern.match(f)]))
    

    

    exampleFile = 'Well'+well[-1]+'_Seq'+sequence[-1]+'t'+times[-1]+well[-1]+'_'+sites[-1]+'c'+channels[-1]+'.tif'
    info = vigra.impex.ImageInfo(exampleFile)
    X, Y, _chan = info.getShape()
    T = int(times[-1])
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
            h5Path = os.path.join(targetDir, 'Well'+well[0]+'_'+ste+'c'+ch+'.h5')
            print('now saving file ' + h5Path)
            with h5py.File(h5Path, 'w') as f:
                dset = f.create_dataset('stacked_timepoints', shape=volume_shape, dtype=dtype, chunks=True)
                dset.attrs['axistags'] = axistags.toJSON()
                for time in times:
                    currFile = 'Well'+well[0]+'_Seq'+sequence[0]+'t'+time+well[0]+'_'+ste+'c'+ch+'.tif'
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
                            dset[int(time)-1,:,:] = img.transpose()
                            print('deleting background-subtracted tif')
                            os.remove(currFile)
                        else:
                            print('resolution does not match resolution of exampleFile, keeping background-subtracted tif')
    os.chdir(previousDirectory)
    return

if __name__ == "__main__":
    #specify parent directory containing wells. Code assumes that it includes backslashes at the end.
    directory = '/awlab/users/jchang/plates/2017_11_10_expt_15_SK_dose_response'
    newDirectory = '/awlab/users/jchang/raw_data/2017_11_10_expt_15_SK_dose_response_h5'
    print('parent source directory to process: {}'.format(directory))
    print('parent target directory to process: {}'.format(newDirectory))

#    directory = r'/awlab/users/jchang/temp/B02'
#    newDirectory = r'/awlab/users/jchang/temp/target'
    
    if not os.path.exists(newDirectory):
        os.makedirs(newDirectory)
    wellRegExp = re.compile('[A-H]\d\d')
    subDirectories = sorted([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)) & bool(wellRegExp.match(name))])
    print('all subdirectories: {}'.format(subDirectories))
    for subDir in subDirectories[7:]:
        sourceDir = os.path.join(directory, subDir)
        targetDir = os.path.join(newDirectory, subDir)
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        processDirectory(sourceDir, targetDir)
 