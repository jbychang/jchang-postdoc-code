setBatchMode(true)
//v = newArray("C04", "C05", "C06", "C07", "C08", "C09", "D04", "D05", "D06", "D07", "D08", "D09", "E04","E05", "E06", "E07", "E08", "E09", "F04", "F05", "F06", "F07", "F08", "F09");
//v = newArray("E06", "E07", "E08", "E09", "F04", "F05", "F06", "F07", "F08", "F09");
//v = newArray("A2", "A3", "A4", "A5", "A6", "A7", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12");
v = newArray("B1_", "C1_", "D1_", "F1_", "G1_");
    for (i=0; i<v.length; i++) {   
	run("Image Sequence...", "open=[/Volumes/westerndigital/research-krogan-aw/nikon microscope images/JC_160729_washout_plate_2016026015_1] number=721 starting=1 increment=1 scale=100 file="+v[i]+" sort");
	run("Subtract Background...", "rolling=50 light sliding stack");
	setMinAndMax(65011, 65535);
	run("Make Montage...", "columns=9 rows=1 scale=1 first=1 last=9 increment=1 border=0 font=70 label use");
	saveAs("Jpeg", "/Volumes/westerndigital/research-krogan-aw/nikon microscope images/JC_160729_washout_plate_2016026015_1/2016026015_1_"+v[i]+"_montage.jpg");
	close("*");
    }
