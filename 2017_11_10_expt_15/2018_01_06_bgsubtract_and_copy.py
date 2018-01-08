# -*- coding: utf-8 -*-
"""
This version of the macro takes all .tifs that don't contain "c1.tif" and does background subtraction on them all, saving them as "filename-bg.tif" in the target directory, then deletes all the .tifs in the target directory (since they will be saved as .h5).
"""

import os
import sys
# import re
# import vigra
# import h5py

if __name__ == "__main__":
    sourceDir = sys.argv[1]
    well = os.path.basename(os.path.normpath(sourceDir))
    targetDir = sys.argv[2]
    macroText = """list = getFileList("{srcDir}");
    
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
                run("Close All");
        }}
     }}""".format(srcDir=sourceDir, trgtDir=targetDir)

    print('writing this ImageJ macro:\n' + macroText)
    print('writing macro to {}'.format(r'/awlab/users/jchang/programs/Fiji.app/macros/tempMacro.ijm'))
    f = open(r'/awlab/users/jchang/programs/Fiji.app/macros/tempMacro_' + well + '.ijm', 'w')
    f.write(macroText)
    f.close()

    print('starting ImageJ...')
    os.environ['LD_LIBRARY_PATH'] = ""
    os.system(
        '{fijiLocation} --allow-multiple --headless --console --plugins ~ -macro /awlab/users/jchang/programs/Fiji.app/macros/tempMacro_{index}.ijm'.format(
            fijiLocation='/awlab/users/jchang/programs/Fiji.app/ImageJ-linux64', index=well))
    os.environ['LD_LIBRARY_PATH'] = '$HOME/glibc-2.14/lib'
    print('ImageJ finished')
