# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import re
import vigra
import h5py


def callRollingBall(fileName, sourceDir):
# This function takes a filename and directory, and returns a background-subtracted numpy array. 
    
#    fileName='test_input.tif'
#    fn=fileName
    macroLines = {'openFile': r'open("'+ sourceDir +'/'+fileName+ r'");', 'subtractBackground': r'run("Subtract Background...", "rolling=100");', 'saveFile': r'saveAs("Tiff", "'+sourceDir+r'/bgSubtractedTemp.tif");'}
    
    rollingBallMacro='{openFile}\n{subtractBackground}\n{saveFile}'.format(**macroLines)
    
    print(rollingBallMacro)
    
    f=open(r'/awlab/users/jchang/programs/Fiji.app/macros/tempMacro.ijm','w')
    f.write(rollingBallMacro)
    f.close()
    print('try to unset LD_LIBRARY_PATH')
    os.environ['LD_LIBRARY_PATH'] = ""
#    os.system('unset LD_LIBRARY_PATH')
    os.system('$LD_LIBRARY_PATH')
    os.system('{fijiLocation} --headless --plugins ~ -macro /awlab/users/jchang/programs/Fiji.app/macros/tempMacro.ijm'.format(fijiLocation='/awlab/users/jchang/programs/Fiji.app/ImageJ-linux64'))
    os.environ['LD_LIBRARY_PATH'] = '$HOME/glibc-2.14/lib'

#open("E:\\plates\\2017_11_10_expt_15\\C05\\WellC05_Seq0010t164C05_0000c3.tif");
#run("Subtract Background...", "rolling=100");
#saveAs("Tiff", "E:\\plates\\2017_11_10_expt_15\\C05\\testimg.tif");
    
    return
    
def processDirectory(sourceDir, targetDir):
#    First, figure out what the well and sequence #, and site number are. Set up a regular expression and capture the groups. Note that this script assumes that there are three digits in the time.
    previousDirectory = os.getcwd()
    os.chdir(sourceDir)
    
    pattern = re.compile(r'Well([A-Z]\d\d)_Seq(\d+)t(\d+)[A-Z]\d\d_(\d+)c([0-9]).tif')
    allFiles = os.listdir(sourceDir)
    well = list(set([pattern.match(f).group(1) for f in allFiles if pattern.match(f)]))
    sequence = list(set([pattern.match(f).group(2) for f in allFiles if pattern.match(f)]))
    times = sorted(set([pattern.match(f).group(3) for f in allFiles if pattern.match(f)]))
    sites = sorted(set([pattern.match(f).group(4) for f in allFiles if pattern.match(f)]))
    channels = sorted(set([pattern.match(f).group(5) for f in allFiles if pattern.match(f)]))
    
    print('previousDirectory = {}'.format(previousDirectory))
    print('sourceDir = {}'.format(sourceDir))
    print('targetDir = {}'.format(targetDir))
    print('well = {}'.format(well))
    print('sequence = {}'.format(sequence))
    

    exampleFile = 'Well'+well[0]+'_Seq'+sequence[0]+'t'+times[0]+well[0]+'_'+sites[0]+'c'+channels[0]+'.tif'
    info = vigra.impex.ImageInfo(exampleFile)
    X, Y, _chan = info.getShape()
    T = len(times)
    dtype = info.getDtype()
    volume_shape = (T, Y, X)
    axistags = vigra.defaultAxistags('tyx')
    
#    print((X, Y, T, dtype))
    
    for ste in sites:
        for ch in channels:
            h5Path = os.path.join(targetDir, 'Well'+well[0]+'_'+ste+'c'+ch+'.h5')
            print(h5Path)
            with h5py.File(h5Path, 'w') as f:
                dset = f.create_dataset('stacked_timepoints', shape=volume_shape, dtype=dtype, chunks=True)
                dset.attrs['axistags'] = axistags.toJSON()
                for time in times:
                    currFile = 'Well'+well[0]+'_Seq'+sequence[0]+'t'+time+well[0]+'_'+ste+'c'+ch+'.tif'
                    print(currFile)
#                    print(time)
#                    print(ch)
#                    print(T)
#                    print(volume_shape)
#                    print(times)
                    if ch != '1':    
                        callRollingBall(currFile, sourceDir)
                        img = vigra.impex.readImage('bgSubtractedTemp.tif', dtype='NATIVE')
                    else: 
                        img = vigra.impex.readImage(currFile, dtype='NATIVE')
#                        print('skipped')
                    dset[int(time)-1,:,:] = img.transpose()
    os.chdir(previousDirectory)
    return

if __name__ == "__main__":
    #specify parent directory containing wells. Code assumes that it includes backslashes at the end.
    directory = '/awlab/users/jchang/plates/2017_11_10_expt_15_SK_dose_response'
    newDirectory = '/awlab/users/jchang/plates/2017_11_10_expt_15_SK_dose_response_h5'
    
    if not os.path.exists(newDirectory):
        os.makedirs(newDirectory)
    wellRegExp = re.compile('[A-H]\d\d')
    subDirectories = sorted([name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name)) & bool(wellRegExp.match(name))])
    print(subDirectories)
    for subDir in subDirectories[10:11]:
        sourceDir = os.path.join(directory, subDir)
        targetDir = os.path.join(newDirectory, subDir)
        if not os.path.exists(targetDir):
            os.makedirs(targetDir)
        print('targetDir = {}'.format(targetDir))
        processDirectory(sourceDir, targetDir)
    
#    callRollingBall('WellC02_Seq0007t077C02_0001c2.tif', directory)
    
  