function output = countPixelsWrapper_2016_03_16
tic
% !powercfg /x /standby-timeout-ac 0
parentDirectory = uigetdir;


% ***Note that if you change tableColumns, you need to change the
% corresponding "structToAdd" line in countPixels too***
% Also note that you will have to change the format in countPixels to match the number of digits in each filename
tableColumns = {'Timepoint', 'Field', 'Green_pixel_intensities', 'Red_pixel_intensities', 'Mask_size', 'NumObjects', 'Directory'};

% initialize table  
T = cell2table(cell(0,size(tableColumns,2)),'VariableNames', tableColumns);

% get all sub directories
oldDir = cd(parentDirectory);
% pathsToAnalyze.name = parentDirectory;
pathsToAnalyze = rdir(fullfile(parentDirectory,'**','*'), 'isdir==1');
pathsToAnalyze(end+1).name = parentDirectory;

for currDir={pathsToAnalyze.name}
%     is the directory empty?
    if size(dir(currDir{1}),1)<3
        continue
    end
    try
        T = countPixels_2016_03_16(currDir{1}, T);
    catch
        %         if there's an error, write the current table to a file, and output the paths and the current directory being analyzed.
        disp('error')
        toc
        datetime('now')
        writetable(T,strcat(date,'-partial_analysis.csv'));
        output = [{pathsToAnalyze} {currDir}];
        cd(oldDir);
        return
    end
    
end

writetable(T,strcat(date,'-output.csv'));
cd(oldDir);
toc
datetime('now')
output = T;
% !powercfg /x /standby-timeout-ac 30
disp('completed successfully')




end