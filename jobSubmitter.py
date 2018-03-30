# Script to submit jobs to QB3 clusters
#
#
#
#
#
# Chien-Hsiang Hsu, 2015.12.18

import sys
import os
import glob
import re
from itertools import groupby
##########################################################################
# Set up

job_size = 1;
runTime = r'10:00:00'
shell_script_mode = True; # Generate shell scripts for commands or not.
                          # It helps when commands contain multiple single/double quotes.



##########################################################################
## Paths
jobScript = os.path.join("/netapp","home",os.getlogin(),"batch.tmp")
outputPath = os.path.join("/netapp","home",os.getlogin(),"cluster","output")
errorPath = os.path.join("/netapp","home",os.getlogin(),"cluster","error")
shell_script_folder = os.path.join("/netapp","home",os.getlogin(),"batch_shell")



def CmdsParser(cmds_file):    
    return ["'"+cmd.rstrip('\n').replace("\r","")+"'" for cmd in open(cmds_file,'r')]



def Cmds2ShellScripts(cmds_file, job_size, job_prefix, shell_script_folder):
    cmds = [cmd.rstrip('\n').replace("\r","") for cmd in open(cmds_file,'r')]

    ## Group every job_size commands. 
    commandsGrouped = [cmds[c:c+job_size] for c in range(0,len(cmds),job_size)]

    ## Write to shell scripts and generate commands to submit
    new_cmds = []
    counter = 1
    for cmd_grp in commandsGrouped:
        shell_script_name = job_prefix + "_" + str(counter) + ".sh"
        sh_path = os.path.join(shell_script_folder,shell_script_name)

        ## 1. Generate shell scripts
        with open(sh_path, 'w') as f:
            for cmd in cmd_grp:
                f.write(cmd+"\n")

        ## 2. Generate commands to execute shell scripts
        new_cmds.append("'sh " + sh_path + "'")

        counter+=1

    return new_cmds



def JobWriter(cmds,job_prefix):        
    # Generate the script and submit the job
    with open(jobScript, 'w') as f:
        
        f.write(r'#!/bin/bash'+"\n")
        f.write("#\n")
        f.write(r'#$ -S /bin/bash'+"\n")
        f.write(r'#$ -N '+job_prefix+"\n")
        f.write(r'#$ -o '+os.path.join(outputPath, job_prefix+".out")+"\n")
        f.write(r'#$ -e '+os.path.join(errorPath, job_prefix+".err")+"\n")
        f.write(r'#$ -cwd'+"\n")
        f.write(r'#$ -r y'+"\n")
        f.write(r'#$ -j y'+"\n")
        f.write(r'#$ -l mem_free=12G'+"\n")
        f.write(r'#$ -l xe5-2680v4=true'+"\n")
        f.write(r'#$ -l arch=linux-x64'+"\n")
        f.write(r'#$ -l netapp=100G,scratch=100G'+"\n")
        f.write(r'#$ -l h_rt='+runTime+"\n")
        f.write(r'#$ -t 1-'+str(len(cmds))+"\n")            

        f.write("\n\n\n\n\n")
        
        # Initialize jobArray
        f.write("jobs=(0 "+ ' '.join(cmds)+")\n")
        
        # Create a bash for loop to perform commands
        f.write(r'${jobs[$SGE_TASK_ID]}'+"\n")
        

        f.write("\n\n\n")

        f.write("date\n")
        
        f.write("hostname\n\n")

        f.write(r'qstat -j $JOB_ID')
        


if __name__ == "__main__":
    cmds_file = sys.argv[1];
    job_prefix = os.path.basename(cmds_file).strip().split('.')[0]

    # 1. Check whether output folders for cluster report exist
    if not os.path.isdir(outputPath):
        os.makedirs(outputPath);
    
    if not os.path.isdir(errorPath):
        os.makedirs(errorPath);    
    

    # 2. Parse cmds_file and generate commands
    if shell_script_mode: # generate shell scripts for commands
        if not os.path.isdir(shell_script_folder):
            os.makedirs(shell_script_folder)

        cmds = Cmds2ShellScripts(cmds_file, job_size, job_prefix, shell_script_folder)


    else: # generate commands from cmds_file        
        cmds = CmdsParser(cmds_file)


    # 3. Generate the job script
    JobWriter(cmds, job_prefix)


    # 4. Submit the job
    os.system("qsub " + jobScript)


    
