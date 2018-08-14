# -*- coding: utf-8 -*-
import os
import sys
import re

if __name__ == "__main__":
    #specify parent directory containing wells.
    sourceDirectory = '/awlab/users/jchang/plates/2018_03_05_expt018_SK_FUCCI'
    targetDirectory = '/awlab/users/jchang/raw_data/2018_03_14_expt018_SK_FUCCI_dose_response'
    codeDirectoryInput = '/awlab/users/jchang/code/2018_03_27_expt_18'

    # sourceDirectory = 'E:\\temp'
    # targetDirectory = 'E:\\temp\\saved'
    # codeDirectoryInput = 'E:\\temp'


    if not os.path.exists(targetDirectory):
        os.makedirs(targetDirectory)
    codeDirectory = os.path.join(codeDirectoryInput, 'temp_scripts')
    if not os.path.exists(codeDirectory):
        os.makedirs(codeDirectory)
    print('this script will produce a master shell script in which each line processes one well.')
    print('parent source directory to process: {}'.format(sourceDirectory))
    print('code directory (where the script will be written): {}'.format(codeDirectory))


    wellRegExp = re.compile(r'.*[A-H]\d\d.*')
    wellNames = sorted([name for name in os.listdir(os.path.join(sourceDirectory,'second_timecourse_836')) if os.path.isdir(os.path.join(sourceDirectory, 'second_timecourse_836', name)) & bool(wellRegExp.match(name))])

    # Use this line to only run a few wells for testing:
    # wellNames = wellNames[0:2]

    master_script_path = os.path.join(codeDirectory, 'combine_to_h5_master_script_2018_05_04.py')
    print('all well directories: {}'.format(wellNames))
    print('master script path: {}'.format(master_script_path))

    for counter, wellName in enumerate(wellNames):
        subDirectoryTimeCourse1 = os.path.join(sourceDirectory, 'first_timecourse_636', wellName)
        subDirectoryTimeCourse2 = os.path.join(sourceDirectory, 'second_timecourse_836', wellName)
        targetSubDirectory = os.path.join(targetDirectory, wellName)

        line_to_write=r'source activate py35 && export LD_LIBRARY_PATH=$HOME/glibc-2.14/lib && python ' + os.path.join(codeDirectoryInput,'2018_05_04_combine_to_h5_bf_nuc_draq7_only.py') + ' ' + wellName + ' ' + targetSubDirectory + ' && source deactivate\n'
        if counter == 0:
            f = open(master_script_path, 'w')
            f.write(line_to_write)
        else:
            with open(master_script_path, 'a+') as f:
                f.write(line_to_write)



