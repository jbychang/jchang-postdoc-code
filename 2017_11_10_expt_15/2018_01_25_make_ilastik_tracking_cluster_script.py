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

with open('/awlab/users/jchang/code/2017_11_10_expt_15/temp_scripts/cluster_script_ilastik_auto_tracking_2018_01_25', 'w') as f:
    for subDir in subDirectories:
        directory = os.path.join(parentDirectory, subDir)
        print('in directory ' + directory)
        pattern = re.compile(r'(.*)_Probabilities.h5')
        allFiles = os.listdir(directory)
        probabilityFiles = [pattern.match(f).group(0) for f in allFiles if pattern.match(f)]
        h5Files = [(pattern.match(f).group(1)+'.h5') for f in allFiles if pattern.match(f)]
        print(r'found the following *_Probabilities.h5 files: ' + str(h5Files))
        for h5File, probabilityFile in zip(h5Files, probabilityFiles):
            f.write('/awlab/users/jchang/programs/ilastik-1.3.0b4-Linux/run_ilastik.sh --headless --project=/awlab/users/jchang/code/2017_11_10_expt_15/2018_01_25_ilastik_13b4_track_with_nucview.ilp --raw_data='+ os.path.join(directory, h5File)+' --prediction_maps='+ os.path.join(directory, probabilityFile) + r' --export_source="Object-Identities" --output_filename_format={dataset_dir}\{nickname}_{result_type}'+'\n')
            f.write('/awlab/users/jchang/programs/ilastik-1.3.0b4-Linux/run_ilastik.sh --headless --project=/awlab/users/jchang/code/2017_11_10_expt_15/2018_01_25_ilastik_13b4_track_with_nucview.ilp --raw_data=' + os.path.join(directory, h5File) + ' --prediction_maps=' + os.path.join(directory, probabilityFile) + r' --export_source="Tracking-Result" --output_filename_format={dataset_dir}\{nickname}_{result_type}' + '\n')
            f.write('/awlab/users/jchang/programs/ilastik-1.3.0b4-Linux/run_ilastik.sh --headless --project=/awlab/users/jchang/code/2017_11_10_expt_15/2018_01_25_ilastik_13b4_track_with_nucview.ilp --raw_data=' + os.path.join(directory, h5File) + ' --prediction_maps=' + os.path.join(directory, probabilityFile) + r' --export_source="Plugin" --export_plugin="CSV-Table" --output_filename_format={dataset_dir}\{nickname}_{result_type}' + '\n')