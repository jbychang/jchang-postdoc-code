import os
import sys
import re
import glob

# This purpose of this script is to make a bash script that can be submitted with jobSubmitter.py. Each line of the bash script will run the Ilastik pixel classification project on a site.

#specify parent directory containing wells. Code assumes that it includes backslashes at the end.
parentDirectory = '/awlab/users/jchang/raw_data/2017_11_10_expt_15_SK_dose_response_h5'   
print('parent directory to process: {}'.format(parentDirectory))

    
wellRegExp = re.compile('[A-H]\d\d')
subDirectories = sorted([name for name in os.listdir(parentDirectory) if os.path.isdir(os.path.join(parentDirectory, name)) & bool(wellRegExp.match(name))])
print('all subdirectories: {}'.format(subDirectories))

with open('/awlab/users/jchang/code/2017_11_10_expt_15/cluster_script_ilastik_pixclass_2018_01_02', 'w') as f:
    for subDir in subDirectories[40:]:
        directory = os.path.join(parentDirectory, subDir)
        print('in directory ' + directory)
        h5Files = glob.glob(os.path.join(directory, r'*c1-2.h5'))
        print(r'found the following *c1-2.h5 files: ' + str(h5Files))
        for h5File in h5Files:
            f.write('/awlab/users/jchang/programs/ilastik-1.3.0b3-Linux/run_ilastik.sh --headless --project=/awlab/users/jchang/code/2017_11_10_expt_15/2018_01_02_ilastik13b4_pixclass.ilp '+ os.path.join(directory, h5File)+'\n')

    