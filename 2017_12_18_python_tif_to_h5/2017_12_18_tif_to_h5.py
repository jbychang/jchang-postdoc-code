# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os

#print(os.getcwd())

def callRollingBall(fileName, directory):
    
    fileName='test_input.tif'
    fn=fileName
    rollingBallMacro='{openFile}\n{subtractBackground}\n{saveFile}'.format(openFile='open(\"E:\\plates\\2017_11_10_expt_15\\C05\\WellC05_Seq0010t164C05_0000c3.tif\");'+fn, subtractBackground='run(\"Subtract Background...\", "rolling=100\");',saveFile='test_save_file')
    f=open('macro.ijm','w')
    f.write(rollingBallMacro)
    f.close()


#open("E:\\plates\\2017_11_10_expt_15\\C05\\WellC05_Seq0010t164C05_0000c3.tif");
#run("Subtract Background...", "rolling=100");
#saveAs("Tiff", "E:\\plates\\2017_11_10_expt_15\\C05\\testimg.tif");
    
    return(1)
    
def processDirectory(directory):
    