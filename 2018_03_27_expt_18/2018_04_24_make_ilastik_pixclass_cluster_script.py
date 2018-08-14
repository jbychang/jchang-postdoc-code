import os
import sys
import re
import glob

# This purpose of this script is to make a bash script that can be submitted with jobSubmitter.py. Each line of the bash script will run the Ilastik pixel classification project on a site.

#specify parent directory containing wells. Code assumes that it includes backslashes at the end.
parentDirectory = '/awlab/users/jchang/raw_data/2018_03_14_expt018_SK_FUCCI_dose_response'
print('parent directory to process: {}'.format(parentDirectory))


wellRegExp = re.compile(r'.*[A-H]\d\d.*')
subDirectories = sorted([name for name in os.listdir(parentDirectory) if os.path.isdir(os.path.join(parentDirectory, name)) & bool(wellRegExp.match(name))])
print('all subdirectories: {}'.format(subDirectories))

with open('/awlab/users/jchang/code/2018_03_27_expt_18/temp_scripts/cluster_script_ilastik_pixclass_2018_05_02', 'w') as f:
    for subDir in subDirectories:
        directory = os.path.join(parentDirectory, subDir)
        print('in directory ' + directory)
        h5Files = glob.glob(os.path.join(directory, r'*000[0-1].h5'))
        print(r'found the following *bf_nuc_nucview*.h5 files: ' + str(h5Files))
        for h5File in h5Files:
            f.write('/awlab/users/jchang/programs/ilastik-1.3.0-Linux/run_ilastik.sh --headless --project=/awlab/users/jchang/code/2018_03_27_expt_18/2018_05_01_ilastik_pixclass_expt18.ilp '+ os.path.join(directory, h5File)+'\n')