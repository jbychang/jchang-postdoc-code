setBatchMode(true)
//v = newArray("C04", "C05", "C06", "C07", "C08", "C09", "D04", "D05", "D06", "D07", "D08", "D09", "E04","E05", "E06", "E07", "E08", "E09", "F04", "F05", "F06", "F07", "F08", "F09");
//v = newArray("E06", "E07", "E08", "E09", "F04", "F05", "F06", "F07", "F08", "F09");
//v = newArray("A2", "A3", "A4", "A5", "A6", "A7", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9", "G10", "G11", "G12");
v = newArray("B06_", "B07_", "B08_", "B09_", "B10_", "B11_", "C06_", "C07_", "C08_", "C09_", "C10_", "C11_", "D06_", "D07_", "D08_", "D09_", "D10_", "D11_", "E06_", "E07_", "E08_", "E09_", "E10_", "E11_", "F06_", "F07_", "F08_", "F09_", "F10_", "F11_", "G06_", "G07_", "G08_", "G09_", "G10_", "G11_");
    for (i=0; i<v.length; i++) {   
	run("Image Sequence...", "open=Y:\\JC_160918_addiction_plate_2016_2016026021_exported\\JC_160918_plate_2016026021_t1_09_18_afterwasB06_0000c1.tif file="+v[i]+" sort");
	run("Subtract Background...", "rolling=50 light sliding stack");
	setMinAndMax(51833, 65403);
	run("Make Montage...", "columns=8 rows=1 scale=1 first=1 last=8 increment=1 border=0 font=70 label");
	saveAs("Jpeg", "Y:\\JC_160918_addiction_plate_2016_2016026021_exported\\montages\\JC_160918_plate_2016026021_"+v[i]+"_montage.jpg");
	close("*");
    }
