# @File(label = "Input directory", style = "directory") input
# @File(label = "Output directory", style = "directory") output
# @String(label = "File suffix", value = ".tif") suffix

run("Close All");

processFolder(input);
print("");
print("PROCESSING FINISHED");

// function to scan folders/subfolders/files to find files with correct suffix
function processFolder(input) {
	list = getFileList(input);
	list = Array.sort(list);
	for (i = 0; i < list.length; i++) {
		if(File.isDirectory(input + list[i])) {
			processFolder("" + input + list[i]);
		}
		
		if(endsWith(list[i], suffix)) {
			processFile(input, output, list[i]);
			run("Close All");
		}	
	}
	selectWindow("Log");
	saveAs("Text", output + "\\" + "Log.txt");
}

function processFile(input, output, file) {
	// Check which options are chosen and act accordingly
	substack = output + "\\" + "Substacks";
	threshold = output + "\\" + "Threshold";
	centroid = output + "\\" + "Centroid maps";
	centres = output + "\\" + "Centres of mass";
	surface = output + "\\" + "Surface maps";
	objects = output + "\\" + "Object maps";
	masked = output + "\\" + "Masked images";
	statistics= output + "\\" + "Statistics";
	
	File.makeDirectory(substack);
		if (!File.exists(substack)) {
			exit("Unable to create Substack directory");
		}
	File.makeDirectory(threshold);
		if (!File.exists(threshold)) {
			exit("Unable to create Threshold directory");
		}
	File.makeDirectory(centroid);
		if (!File.exists(centroid)) {
			exit("Unable to create Centroid maps directory");
		}
	File.makeDirectory(centres);
		if (!File.exists(centres)) {
			exit("Unable to create Centres of mass directory");
		}
	File.makeDirectory(surface);
		if (!File.exists(surface)) {
			exit("Unable to create Surface maps directory");
		}
	File.makeDirectory(objects);
		if (!File.exists(objects)) {
			exit("Unable to create Object maps directory");
		}
	File.makeDirectory(masked);
		if (!File.exists(masked)) {
			exit("Unable to create Masked images directory");
		}		
	File.makeDirectory(statistics);
		if (!File.exists(statistics)) {
			exit("Unable to create Statistics directory");
		}				
	
	//setBatchMode(true);
	print(" ");
	print("Processing: " + input + "\\" + file);
	open(input + "\\" + list[i]);
	//run("Bio-Formats Importer", "open=[" + input + "\\" + list[i] + "]"); //alternative opener, produced bad thresholds
	
		makeSubstack(input, output, file, substack);
		createThreshold(input, output, file, threshold);
		start3DOC(input, output, file, centroid, centres, surface, objects, masked, statistics);
		
	//setBatchMode(false);
}

function makeSubstack(input, output, file, substack) {
	print("Creating Substack of: " + input + "\\" + file);
	makeRectangle(17, 64, 905, 468);
	run("Crop");
	run("Duplicate...", "duplicate range=49-596");
	run("16-bit");
	run("Properties...", "channels=1 slices=548 frames=1 unit=um pixel_width=0.645 pixel_height=0.645 voxel_depth=0.645 origin=0,0,0");
	saveAs("Tiff", substack + "\\" + "Substack-" + list[i]);
	selectWindow(list[i]);
	close();
}

function createThreshold(input, output, file, threshold) {
	print("Creating Threshold of: " + input + "\\" + file);
	run("Duplicate...", "duplicate");
	setAutoThreshold("Default dark");
	//run("Threshold...");
	setAutoThreshold("Default dark stack");
	setThreshold(8487, 65535);
	setOption("BlackBackground", false);
	run("Convert to Mask", "method=Default background=Dark black");
	saveAs("Tiff", threshold + "\\" + "Threshold-" + list[i]);
}

function start3DOC(input, output, file, centroid, centres, surface, objects, masked, statistics) {
	print("Running 3DOC for: " + input + "\\" + file);
	run("3D OC Options", "volume surface nb_of_obj._voxels nb_of_surf._voxels integrated_density mean_gray_value std_dev_gray_value median_gray_value minimum_gray_value maximum_gray_value centroid mean_distance_to_surface std_dev_distance_to_surface median_distance_to_surface centre_of_mass bounding_box show_masked_image_(redirection_requiered) dots_size=5 font_size=10 show_numbers white_numbers store_results_within_a_table_named_after_the_image_(macro_friendly) redirect_to=Substack-" + list[i]);
	run("3D Objects Counter", "threshold=128 slice=261 min.=150 max.=4000 exclude_objects_on_edges objects surfaces centroids centres_of_masses statistics summary");
	selectWindow("Centroids map of Threshold-" + list[i] + " redirect to Substack-" + list[i]);
	saveAs("Tiff", centroid + "\\" + "Centroids map of Threshold-" + list[i] + " redirect to Substack-" + list[i]);
	selectWindow("Centres of mass map of Threshold-" + list[i] + " redirect to Substack-" + list[i]);
	saveAs("Tiff", centres + "\\" + "Centres of mass map of Threshold-" + list[i] + " redirect to Substack-" + list[i]);
	selectWindow("Surface map of Threshold-" + list[i] + " redirect to Substack-" + list[i]);
	saveAs("Tiff", surface + "\\" + "Surface map of Threshold-" + list[i] + " redirect to Substack-" + list[i]);
	selectWindow("Objects map of Threshold-" + list[i] + " redirect to Substack-" + list[i]);
	saveAs("Tiff", objects + "\\" + "Objects map of Threshold-" + list[i] + " redirect to Substack-" + list[i]);
	selectWindow("Masked image for Threshold-" + list[i] + " redirect to Substack-" + list[i]);
	saveAs("Tiff", masked + "\\" + "Masked image for Threshold-" + list[i] + " redirect to Substack-" + list[i]);
	selectWindow("Statistics for Threshold-" + list[i] + " redirect to Substack-" + list[i]);
	saveAs("Results", statistics + "\\" + "Statistics for Threshold-" + list[i] + " redirect to Substack-" + list[i] + ".xls");
}
