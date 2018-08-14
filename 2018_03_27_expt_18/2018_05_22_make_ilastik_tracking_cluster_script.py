import os
import sys
import re
import glob

# This purpose of this script is to make a bash script that can be submitted with jobSubmitter.py. Each line of the bash script will run the Ilastik pixel classification project on a site.

#specify parent directory containing wells. Code assumes that it includes backslashes at the end.
parentDirectory = '/awlab/users/jchang/raw_data/2018_03_14_expt018_SK_FUCCI_dose_response'
ilastikTrackingPath = '/awlab/users/jchang/code/2018_03_27_expt_18/2018_05_18_ilastik_autotrack_three_channels_expt18.ilp'
temp_script_path = '/awlab/users/jchang/code/2018_03_27_expt_18/temp_scripts/cluster_script_ilastik_auto_tracking_2018_05_22'
print('parent directory to process: {}'.format(parentDirectory))


wellRegExp = re.compile(r'.*[A-H]\d\d.*')
subDirectories = sorted([name for name in os.listdir(parentDirectory) if os.path.isdir(os.path.join(parentDirectory, name)) & bool(wellRegExp.match(name))])
print('all subdirectories: {}'.format(subDirectories))

with open(temp_script_path, 'w') as f:
    for subDir in subDirectories:
        directory = os.path.join(parentDirectory, subDir)
        print('in directory ' + directory)
        pattern = re.compile(r'(.*)draq7_Probabilities.h5')
        # NOTE THAT THE REGULAR EXPRESSION IN THE PREVIOUS LINE FINDS DRAQ7-CONTAINING FILES, AND MUST BE CHANGED THREE LINES DOWN AS WELL
        allFiles = os.listdir(directory)
        probabilityFiles = [pattern.match(f).group(0) for f in allFiles if pattern.match(f)]
        h5Files = [(pattern.match(f).group(1)+'draq7.h5') for f in allFiles if pattern.match(f)]
        print(r'found the following *draq7_Probabilities.h5 files: ' + str(h5Files))
        for h5File, probabilityFile in zip(h5Files, probabilityFiles):
            f.write('/awlab/users/jchang/programs/ilastik-1.3.0-Linux/run_ilastik.sh --headless --project=' + ilastikTrackingPath + ' --raw_data='+ os.path.join(directory, h5File)+' --prediction_maps='+ os.path.join(directory, probabilityFile) + r' --export_source="Object-Identities" --output_filename_format={dataset_dir}\{nickname}_{result_type}'+'\n')
            f.write('/awlab/users/jchang/programs/ilastik-1.3.0-Linux/run_ilastik.sh --headless --project=' + ilastikTrackingPath + ' --raw_data=' + os.path.join(directory, h5File) + ' --prediction_maps=' + os.path.join(directory, probabilityFile) + r' --export_source="Tracking-Result" --output_filename_format={dataset_dir}\{nickname}_{result_type}' + '\n')
            f.write('/awlab/users/jchang/programs/ilastik-1.3.0-Linux/run_ilastik.sh --headless --project=' + ilastikTrackingPath + ' --raw_data=' + os.path.join(directory, h5File) + ' --prediction_maps=' + os.path.join(directory, probabilityFile) + r' --export_source="Plugin" --export_plugin="CSV-Table" --output_filename_format={dataset_dir}\{nickname}_{result_type}' + '\n')