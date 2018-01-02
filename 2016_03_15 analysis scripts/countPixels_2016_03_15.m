function output = countPixels_2016_03_15(directory, T)

oldDir = cd(directory);
fileNames = dir('*.tif');
if size(fileNames,1)==0
    %         ***THIS LINE NEEDS TO BE CHANGED IF tableColumns IS CHANGED***
    structToAdd = struct('Timepoint', 0, 'Field', 0, 'Green_pixel_intensities', 0,...
        'Red_pixel_intensities', 0, 'Mask_size', 0, 'NumObjects', 0, 'Directory', {{directory}});
    T = [T;struct2table(structToAdd)];
    output = T;
    return
end

idx = 1;
images = struct([]);
for fn = {fileNames.name}
    pattern = '(.*)t([0-9]+)c([0-9])';
    [tokens, matches] = regexp(fn,pattern,'tokens','match');
    if ~isempty(matches{1})
        images(idx).rootName = tokens{1}{1}{1};
        images(idx).timePoint = tokens{1}{1}{2};
        images(idx).colorIndex = tokens{1}{1}{3};
        images(idx).fieldIndex = 0;
        images(idx).fullName = fn;
        idx = idx + 1;
    end
end


for tp = 1:max(str2num(str2mat({images.timePoint})))
    %     for field = 1:max(str2num(str2mat({images.fieldIndex})))
    
    imgGreen = imread(sprintf('%st%02dc2.tif',images(1).rootName, tp));
    imgRed = imread(sprintf('%sT%02dC3.tif',images(1).rootName, tp));
    imgg_bg=imtophat(imgGreen,offsetstrel('ball',50,100));
    imgg_bg_cont=imadjust(imgg_bg,stretchlim(imgg_bg,0),[]);
    imgr_bg=imtophat(imgRed,offsetstrel('ball',50,100));
    imgr_bg_cont=imadjust(imgr_bg,stretchlim(imgr_bg,0),[]);
    % RED
    hy = fspecial('sobel');
    hx = hy';
    Iy = imfilter(double(imgr_bg_cont), hy, 'replicate');
    Ix = imfilter(double(imgr_bg_cont), hx, 'replicate');
    gradmag = sqrt(Ix.^2 + Iy.^2);
    
    levelsr = double(multithresh(imgr_bg_cont,20));
    imgrt = im2bw(imgr_bg_cont,levelsr(2)/double(2^16));
%     imshowpair(imadjust(imgr_bg_cont),imgrt)
%     imgrt = im2bw(imgr_bg,thresholdFluorescenceImage(imgr_bg)/2^16);
    imgrte = imerode(imgrt,strel('disk',5));
    fgm = imgrte;
    % figure
    % imshowpair(imadjust(imgr_bg_cont),imgrte)
    % title('original versus thresholded and eroded')
    
    
    D = bwdist(imgrte);
    DL = watershed(D);
    bgm = DL == 0;
    gradmag2 = imimposemin(gradmag, bgm | fgm);
    Lred = watershed(gradmag2);
    %         get rid of unreasonably large regions
    bwccred = bwconncomp(Lred);
    [nrows, ncols]= cellfun(@size,bwccred.PixelIdxList);
    unreasonable_size=find(nrows>1000);
    if size(unreasonable_size,2)~=1
        unreasonable_size=unreasonable_size(2:end);
        for i=1:size(unreasonable_size,2)
            Lred(bwccred.PixelIdxList{unreasonable_size(i)})=0;
        end
    end
    
    %         green
    hy = fspecial('sobel');
    hx = hy';
    Iy = imfilter(double(imgg_bg_cont), hy, 'replicate');
    Ix = imfilter(double(imgg_bg_cont), hx, 'replicate');
    gradmag = sqrt(Ix.^2 + Iy.^2);
    
    imggt = im2bw(imgg_bg_cont,graythresh(imgg_bg_cont));
    imggte = imerode(imggt,strel('disk',5));
    % figure
    % imshowpair(imadjust(imgg_bg_cont),imggte)
    % title('original versus thresholded and eroded')
    
    fgm = imggte;
    
    D = bwdist(imggte);
    DL = watershed(D);
    bgm = DL == 0;
    %         imshowpair(imggte,bgm)
    gradmag2 = imimposemin(gradmag, bgm | fgm);
    Lgreen = watershed(gradmag2);
    
    %         get rid of unreasonably large regions
    bwccgreen = bwconncomp(Lgreen);
    [nrows, ncols]= cellfun(@size,bwccgreen.PixelIdxList);
    unreasonable_size=find(nrows>1000);
    if size(unreasonable_size,2)~=1
        unreasonable_size=unreasonable_size(2:end);
        for i=1:size(unreasonable_size,2)
            Lgreen(bwccgreen.PixelIdxList{unreasonable_size(i)})=0;
        end
    end
    %         both
    BWmask = Lred+Lgreen;
    BWmask(BWmask==2)=0;
    BWmask(BWmask>2)=1;
    BWmask = uint16(BWmask);
    maskedGreen = BWmask.*imgg_bg_cont;
    maskedRed = BWmask.*imgr_bg_cont;
    
    maskedintensityGreen = sum(maskedGreen(:));
    maskedintensityRed = sum(maskedRed(:));
    numPx = sum(BWmask(:));
    CC = bwconncomp(BWmask);
    
    
    %         ***THIS LINE NEEDS TO BE CHANGED IF tableColumns IS CHANGED***
    structToAdd = struct('Timepoint', tp, 'Field', 0, 'Green_pixel_intensities', maskedintensityGreen,...
        'Red_pixel_intensities', maskedintensityRed, 'Mask_size', numPx, 'NumObjects', CC.NumObjects, 'Directory', {{directory}});
    
    
    T = [T;struct2table(structToAdd)];
    output = T;
    Lred(Lred==1)=0;
    Lgreen(Lgreen==1)=0;
    mergedLabels = Lred+(Lgreen+max(Lred(:)));
    imwrite(label2rgb(mergedLabels), sprintf('%sT%02dmask.png',images(1).rootName, tp));
    
    
    %     end
end

cd(oldDir);
end

