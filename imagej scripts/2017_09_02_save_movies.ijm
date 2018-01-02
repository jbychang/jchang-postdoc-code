//dir1 = getDirectory("Choose Source Directory ");
dir2 = getDirectory("Choose Output Directory ");
//channel = 1;
//filename = 'test';
//Dialog.create("Select channel");
//Dialog.addString("Channel: (0, 1, 2...)", channel);
//Dialog.addString("Filename: (0, 1, 2...)", filename);
//Dialog.show();
//channel = Dialog.getString();
//filename = Dialog.getString();
//print(channel);
//print(filename);

fields = newArray("B2_0000","B3_0000","B4_0000","B5_0000","B6_0000","B7_0000","B8_0000","B9_0000","B10_0000","B11_0000","C2_0000","C3_0000","C4_0000","C5_0000","C6_0000","C7_0000","B2_0001","B3_0001","B4_0001","B5_0001","B6_0001","B7_0001","B8_0001","B9_0001","B10_0001","B11_0001","C2_0001","C3_0001","C4_0001","C5_0001","C6_0001","C7_0001");

for (i=0; i<fields.length; i++) {  
	
//run("Bio-Formats Importer", "open=Z:\\JC_170822_plate_2017026104_tlapse_10min\\flatfiles\\JC_20170822_plate_2017026104_tlapse_10min_t001_B2_0000-1.tif autoscale color_mode=Default group_files rois_import=[ROI manager] specify_range view=Hyperstack stack_order=XYCZT swap_dimensions axis_1_number_of_images=2 axis_1_axis_first_image=1 axis_1_axis_increment=1 axis_2_number_of_images=2 axis_2_axis_first_image=2 axis_2_axis_increment=1 axis_3_number_of_images=2 axis_3_axis_first_image=0 axis_3_axis_increment=1 axis_4_number_of_images=4 axis_4_axis_first_image=1 axis_4_axis_increment=1 contains=[] name=D:\\jbchang\\temp_ij\\JC_20170822_plate_2017026104_tlapse_10min_t00<1-2>_<B2_0000,B3_0000,B4_0000,B5_0000,B6_0000,B7_0000,B8_0000,B9_0000,B10_0000,B11_0000,C2_0000,C3_0000,C4_0000,C5_0000,C6_0000,C7_0000,B2_0001,B3_0001,B4_0001,B5_0001,B6_0001,B7_0001,B8_0001,B9_0001,B10_0001,B11_0001,C2_0001,C3_0001,C4_0001,C5_0001,C6_0001,C7_0001>-<1-4>.tif z_1=8 c_1=4 t_1=2 c_begin=1 c_end=4 c_step=1 z_begin=1 z_end=1 z_step=1 t_begin=1 t_end=2 t_step=1");

run("Image Sequence...", "open=E:\\Jeremy\\JC_170822_plate_2017026104_tlapse_10min\\JC_20170822_plate_2017026104_tlapse_10min_t001_B2_0000-1.tif file="+fields[i]+" convert sort");
rename("cells");
run("Deinterleave", "how=4 keep");

//run("Split Channels");
selectWindow("cells #1");
//run("Subtract Background...", "paraboloid=20000 light stack");
//run("Subtract Background...", "paraboloid=20000 stack");
setMinAndMax(22, 255);
//setSlice(15);
//run("Enhance Contrast", "saturated=0.35");

selectWindow("cells #2");
run("Subtract Background...", "rolling=500 stack");
//run("Subtract Background...", "paraboloid=20000 stack");
setMinAndMax(0, 70);
//run("Enhance Contrast", "saturated=0.35");

selectWindow("cells #3");
//run("Subtract Background...", "paraboloid=20000 stack");
run("Subtract Background...", "rolling=500 stack");
setMinAndMax(0, 255);
//resetMinAndMax();


selectWindow("cells #4");
run("Subtract Background...", "rolling=500 stack");
//run("Subtract Background...", "paraboloid=20000 stack");
setMinAndMax(0, 255);
//resetMinAndMax();

//run("Merge Channels...", "c1=[C3-cells] c2=[C2-cells] c4=[C1-cells] create keep");

//run("Merge Channels...", "c1=C4-cells c2=C3n-cells c4=C1-cells c5=C2-cells create keep");
//run("Merge Channels...", "c4=C1-cells c5=C2-cells create keep");
run("Merge Channels...", "c1=[cells #4] c2=[cells #3] c4=[cells #1] c5=[cells #2] create keep");
//run("AVI... ", "compression=JPEG frame=7 save=[/Users/jbchang/Desktop/2015_12_14 verbB NaPP1 test about72  h after plating002/2015_12_14 verbB NaPP1 test about72  h after platingXY" + i + ".avi]");
//run("AVI... ", "compression=JPEG frame=7 save=D:\\jbchang\\temp_ij\\test_z2.avi");
run("AVI... ", "compression=JPEG frame=7 save="+dir2+"JC_20170822_plate_2017026104_tlapse_10min_"+fields[i]+".avi");
run("Close All");
};