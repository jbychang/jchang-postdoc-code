function output = countPixelsWrapper_2016_03_15
tic
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
        T = countPixels_2016_03_15(currDir{1}, T);
    catch
%         if there's an error, write the current table to a file, and output the paths and the current directory being analyzed.
        toc
        datetime('now')
        writetable(T,'partial_analysis.csv');
        output = [{pathsToAnalyze} {currDir}];
        pause 
        cd(oldDir);
        return
    end
    
end

writetable(T,strcat(date,'-output.csv'));
cd(oldDir);
toc
datetime('now')
output = T;

% % first, get files in current directory
% files = dir;
%    
% % while there are more directories, continue saving their paths
% moreDirectories = 1;
% while moreDirectories ==1
% 
%     % is the directory empty?
%     if size(files,1)<3
%         moreDirectories = 0;
%         continue
%     end
% 
% %         are there more directories?
%     if max([out(3:end).isdir])==1
%         
%         for fileNum = 3:size(files,1)
%             if files(fileNum).isdir == 1
%                 pathsToAnalyze = [pathsToAnalyze fullfile(currDir,files(fileNum).name)];
%         end
%     end
% end

% 
% 
% iterate through all directories and save output into a file
% output = files;


end