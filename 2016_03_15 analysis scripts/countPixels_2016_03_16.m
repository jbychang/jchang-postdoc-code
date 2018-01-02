function output = countPixels_2016_03_16(directory, T)

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
    
    imgGreen = imread(sprintf('%st%03dc2.tif',images(1).rootName, tp));
    imgRed = imread(sprintf('%sT%03dC3.tif',images(1).rootName, tp));
    imgg_bg=imtophat(imgGreen,offsetstrel('ball',50,100));
    %     imgg_bg_cont=imadjust(imgg_bg,stretchlim(imgg_bg,0),[]);
    imgr_bg=imtophat(imgRed,offsetstrel('ball',50,100));
    %     imgr_bg_cont=imadjust(imgr_bg,stretchlim(imgr_bg,0),[]);
    imgg_bg_d = im2double(imgg_bg);
    imgr_bg_d = im2double(imgr_bg);
    
    
    imgs = imgr_bg_d+3.*(imgg_bg_d.^1.3);
    imgsc = imadjust(imgs,stretchlim(imgs,0),[]);
    % RED
    hy = fspecial('sobel');
    hx = hy';
    Iy = imfilter(imgsc, hy, 'replicate');
    Ix = imfilter(imgsc, hx, 'replicate');
    gradmag = sqrt(Ix.^2 + Iy.^2);
    
    %     for now, using a fixed threshold. maybe a better one would be to
    %     get average foreground and background pixel intensity and use
    %     those to calculate a threshold.
    imgsct = im2bw(imgsc,.06);
    %     imshowpair(imadjust(imgsc),imgsct)
    %     imgrt = im2bw(imgr_bg,thresholdFluorescenceImage(imgr_bg)/2^16);
    %     imgscte = imerode(imdilate(imgsct,strel('disk',2)),strel('disk',6));
    imgscte = imerode(imgsct,strel('disk',4));
    %     imshowpair(imadjust(imgsc),imgscte)
    fgm = imgscte;
    % figure
    % imshowpair(imadjust(imgr_bg_cont),imgrte)
    % title('original versus thresholded and eroded')
    
    
    D = bwdist(imgscte);
    DL = watershed(D);
    bgm = DL == 0;
    gradmag2 = imimposemin(gradmag, bgm | fgm);
    L = watershed(gradmag2);
    
    
    %         get rid of unreasonably large regions
    bwcc = bwconncomp(L);
    [nrows, ncols]= cellfun(@size,bwcc.PixelIdxList);
    big_regions=find(nrows>1000);
    for i=1:size(big_regions,2)
        L(bwcc.PixelIdxList{big_regions(i)})=0;
    end
    
    
    BWmask = L;
    BWmask(BWmask==1)=0;
    BWmask(BWmask>1)=1;
    BWmask = double(BWmask);
    maskedGreen = BWmask.*imgg_bg_d;
    maskedRed = BWmask.*imgr_bg_d;
    maskedintensityGreen = sum(maskedGreen(:));
    maskedintensityRed = sum(maskedRed(:));
    numPx = sum(BWmask(:));
    CC = bwconncomp(BWmask);
    
    
    %         ***THIS LINE NEEDS TO BE CHANGED IF tableColumns IS CHANGED***
    structToAdd = struct('Timepoint', tp, 'Field', 0, 'Green_pixel_intensities', maskedintensityGreen,...
        'Red_pixel_intensities', maskedintensityRed, 'Mask_size', numPx, 'NumObjects', CC.NumObjects, 'Directory', {{directory}});
    
    
    T = [T;struct2table(structToAdd)];
    output = T;
    L(L==1)=0;
    imwrite(label2rgb(L, 'jet', 'k', 'shuffle'), sprintf('%sT%03dmask.png',images(1).rootName, tp));
    
    
    %     end
end

cd(oldDir);
end

