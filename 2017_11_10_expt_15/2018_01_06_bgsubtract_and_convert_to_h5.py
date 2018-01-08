import os
import sys
import re


if __name__ == "__main__":
    #specify parent directory containing wells.
    sourceDirectory = '/awlab/users/jchang/plates/2017_11_10_expt_15_SK_dose_response'
    targetDirectory = '/awlab/users/jchang/raw_data/2017_11_10_expt_15_SK_dose_response_h5'
    codeDirectoryInput = '/awlab/users/jchang/code/2017_11_10_expt_15'

    if not os.path.exists(targetDirectory):
        os.makedirs(targetDirectory)
    codeDirectory = os.path.join(codeDirectoryInput, 'temp_scripts')
    if not os.path.exists(codeDirectory):
        os.makedirs(codeDirectory)
    print('this script will produce a master shell script in which each line processes one well.')
    print('parent source directory to process: {}'.format(sourceDirectory))
    print('code directory (where the script will be written): {}'.format(codeDirectory))


    wellRegExp = re.compile('[A-H]\d\d')
    subDirectories = sorted([name for name in os.listdir(sourceDirectory) if os.path.isdir(os.path.join(sourceDirectory, name)) & bool(wellRegExp.match(name))])
    master_script_path = os.path.join(codeDirectory, 'bgsubtract_convert_combine_master_script_2018_01_06')
    # combine_to_h5_master_script_path = os.path.join(codeDirectory, '2018_01_06_combine_to_h5_master_script')
    print('all subdirectories: {}'.format(subDirectories))
    print('bgsubtract and convert master script path: {}'.format(master_script_path))
    # print('combine to h5 master script path: {}'.format(combine_to_h5_master_script_path))
    for counter, subDir in enumerate(subDirectories):
        subDirectory = os.path.join(sourceDirectory, subDir)
        targetSubDirectory = os.path.join(targetDirectory, subDir)
        if not os.path.exists(targetSubDirectory):
            os.makedirs(targetSubDirectory)
        line_to_write=r'source activate py35 && export LD_LIBRARY_PATH=$HOME/glibc-2.14/lib && python ' + os.path.join(codeDirectoryInput,'2018_01_06_bgsubtract_and_copy.py') + ' ' + subDirectory + ' ' + targetSubDirectory + ' && python ' + os.path.join(codeDirectoryInput, '2018_01_06_combine_to_h5.py') + ' ' + targetSubDirectory + ' 0' + ' ' + '19' + ' && python ' + os.path.join(codeDirectoryInput, '2018_01_06_combine_to_h5.py') + ' ' + targetSubDirectory + ' 19' + ' ' + ':' + ' && source deactivate\n'
        if counter == 0:
            f = open(master_script_path, 'w')
            f.write(line_to_write)
        else:
            with open(master_script_path, 'a+') as f:
                f.write(line_to_write)