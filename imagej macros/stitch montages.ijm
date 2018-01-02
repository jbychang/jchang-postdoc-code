setBatchMode(true);
v = newArray("1", "2", "3", "4", "5", "6", "7", "8", "9");
for (i=0; i<v.length; i++) {
	open("/Users/jbchang/Desktop/JC_160729_washout_plate_2016026015_1 temp/2016026015_1_t"+v[i]+"_wells_B_to_D_montage.jpg");
	open("/Users/jbchang/Desktop/JC_160729_washout_plate_2016026015_1 temp/2016026015_1_t"+v[i]+"_wells_E_to_G_montage.jpg");
	run("Images to Stack", "name=Stack title=[] use");
	run("Make Montage...", "columns=1 rows=2 scale=1 first=1 last=2 increment=1 border=0 font=70");
	saveAs("Tiff", "/Users/jbchang/Desktop/JC_160729_washout_plate_2016026015_1 temp/2016026015_1_t"+v[i]+"_wells_B_to_G_montage.tif");
	run("Close All");
}
