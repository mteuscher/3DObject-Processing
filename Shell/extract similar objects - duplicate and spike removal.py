import os
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--path", help="Path of the statistics files")
parser.add_argument("-s", "--suffix", help="File suffix of statistics files")
parser.add_argument("-f", "--filter", help="Only process files containing a certain string")
parser.add_argument("-r", "--reference", help="Use the following file as a reference")
parser.add_argument("-d", "--debug", help="Also create files that weren't filtered", action="store_true")

args = parser.parse_args()

if args.path != None:
    path = args.path
else:
    print("This script can also be run from the command line. Execute with -h for help")
    path = str(input("Enter Path:"))

if args.suffix != None:
    file_type = args.suffix
else:
    file_type = str(input("Enter file suffix:"))

if args.filter != None:
    name_part = args.filter
else:
    name_part = str(input("Only Process files containing:"))

log = open(os.path.join(path, "log.txt"), "w+")

def sortNames(elem):
    test = elem.split("TP")[1]
    test = test.split("_")[0]
    return test.zfill(3)

def generateFileList(folders, suffix="xls", name_filter=None, recursive=False):
    #Function to test if the found file has the correct suffix
    def check_type(string):
        if suffix:
            if isinstance(suffix, (list, tuple)):
                for suffix_ in suffix:
                    if string.endswith(suffix_):
                        return True
                    else:
                        continue
            elif isinstance(suffix, str):
                if string.endswith(suffix):
                    return True
                else:
                    return False
            return False
        else:
            print("WARNING: ACCEPTING ALL FILE TYPES")
            return True

    def check_filter(string):
        '''This function is used to check for a given filter.
        It is possible to use a single string or a list/tuple of strings as filter.
        This function can access the variables of the surrounding function.
        :param string: The filename to perform the filtering on.
        '''
        if name_filter:
            # The first branch is used if name_filter is a list or a tuple.
            if isinstance(name_filter, (list, tuple)):
                for name_filter_ in name_filter:
                    if name_filter_ in string:
                        # Exit the function with True.
                        return True
                    else:
                        # Next iteration of the for loop.
                        continue
            # The second branch is used if name_filter is a string.
            elif isinstance(name_filter, str):
                if name_filter in string:
                    return True
                else:
                    return False
            return False
        else:
        # Accept all files if name_filter is None.
            return True

    def files_in_folder(folder):
        path_to_images = []
        folder = os.path.expanduser(folder)
        folder = os.path.expandvars(folder)
        
        # If we don't want a recursive search, we can use os.listdir().
        if not recursive:
            for file_name in os.listdir(folder):
                full_path = os.path.join(folder, file_name)
                if os.path.isfile(full_path):
                    if check_type(file_name):
                        if check_filter(file_name):
                            path_to_images.append(full_path)
        # For a recursive search os.walk() is used.
        else:
            # os.walk() is iterable.
            # Each iteration of the for loop processes a different directory.
            # the first return value represents the current directory.
            # The second return value is a list of included directories.
            # The third return value is a list of included files.
            for directory, _, file_names in os.walk(folder):
                # We are only interested in files.
                for file_name in file_names:
                    # The list contains only the file names.
                    # The full path needs to be reconstructed.
                    full_path = os.path.join(directory, file_name)
                    # Both checks are performed to filter the files.
                    if check_type(file_name):
                        if check_filter(file_name):
                            # Add the file to the list of images to open.
                            path_to_images.append(full_path)
        return path_to_images

    final_list = files_in_folder(folders)
    final_list.sort(key=sortNames)
    return final_list

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def process(line):
    if line.split(sep="\t")[11] is not "X":
        if X_temp-8 < float(line.split(sep="\t")[11]) < X_temp+8:
            if Y_temp-8 < float(line.split(sep="\t")[12]) < Y_temp+8:
                if Z_temp-8 < float(line.split(sep="\t")[13]) < Z_temp+8:
                    lineVol = float(line.split(sep="\t")[1])
                    lineMinDist = float(line.split(sep="\t")[17])
                    lineMaxDist = float(line.split(sep="\t")[18])
                    lineRatioDist = float(line.split(sep="\t")[19])
                    lineX = float(line.split(sep="\t")[11])
                    lineY = float(line.split(sep="\t")[12])
                    lineZ = float(line.split(sep="\t")[13])
                    return lineVol, lineMinDist, lineMaxDist, lineRatioDist ,lineX, lineY, lineZ
    
# def analyzeFile(filename):    
#     foundValue = []
#     with open(openFile) as f:
#         for line in f:
#             temp = process(line)
#             if temp is not None:
#                 foundValue.append(temp)
#     f.close()
#     return foundValue

files = generateFileList(path, file_type, name_part)


for file in files:
    print("Timepoint {}: {}".format(files.index(file),file), file=log)

print("---------------------------------------------", file=log)

if args.reference != None:
    referenceTimepoint = int(args.reference)
else:
    print("Detected {} files for Processing".format(len(files)))
    if query_yes_no("Do you want to inspect the files and their order?", default="yes") is True:
        for file in files:
            print("Timepoint {}: {}".format(files.index(file),file))
    referenceTimepoint = int(input("Which Timepoint to use as Reference?:"))

X, Y, Z = [], [], []

f = open(str(files[referenceTimepoint]))
for line in f:
    if line.split(sep="\t")[11] is not "X":
        X.append(float(line.split(sep="\t")[11]))
        Y.append(float(line.split(sep="\t")[12]))
        Z.append(float(line.split(sep="\t")[13]))
f.close()

print("\nYour reference Timepoint is the file: {}\nIt contains {} objects".format(str(files[referenceTimepoint]), len(X)))
print("Your reference Timepoint is the file: {}\nIt contains {} objects".format(str(files[referenceTimepoint]), len(X)), file=log)
if query_yes_no("Do you want to continue?") is False:
    print("Detection aborted")
    print("Detection aborted", file=log)
    log.close()
    sys.exit()

print("---------------------------------------------", file=log)

finalVol = []
finalMinDist = []
finalMaxDist = []
finalRatioDist = []
finalX = []
finalY = []
finalZ = []

header = []
#for file in files:
#    header.append(file.split(os.sep)[-1])
#    
finalVol.append(header)
finalMinDist.append(header)
finalMaxDist.append(header)
finalRatioDist.append(header)
finalX.append(header)
finalY.append(header)
finalZ.append(header)



for entry in X:
    finalVol.append(["NA"])
    finalMinDist.append(["NA"])
    finalMaxDist.append(["NA"])
    finalRatioDist.append(["NA"])
    finalX.append(["NA"])
    finalY.append(["NA"])
    finalZ.append(["NA"])

i=0
while i < len(X):
    X_temp = X[i]
    Y_temp = Y[i]
    Z_temp = Z[i]
    nucleiVol = []
    nucleiMinDist = []
    nucleiMaxDist = []
    nucleiRatioDist = []
    nucleiX = []
    nucleiY = []
    nucleiZ = []
    
    os.system('cls')
    print("Processing value {}/{}".format(i+1,len(X)))
    
    for file in files:
        #result = ["TP{}".format(sortNames(file))]
        resultVol, resultMinDist, resultMaxDist, resultRatioDist, resultX, resultY, resultZ = [], [], [], [], [], [], []

        f = open(str(file))
        for line in f:
            temp = process(line)
            if temp is not None:
                resultVol.append(temp[0])
                resultMinDist.append(temp[1])
                resultMaxDist.append(temp[2])
                resultRatioDist.append(temp[3])
                resultX.append(temp[4])
                resultY.append(temp[5])
                resultZ.append(temp[6])
        nucleiVol.append(resultVol) if not (resultVol == []) else (nucleiVol.append(["NA"]))
        nucleiMinDist.append(resultMinDist) if not (resultMinDist == []) else (nucleiMinDist.append(["NA"]))
        nucleiMaxDist.append(resultMaxDist) if not (resultMaxDist == []) else (nucleiMaxDist.append(["NA"]))
        nucleiRatioDist.append(resultRatioDist) if not (resultRatioDist == []) else (nucleiRatioDist.append(["NA"]))
        nucleiX.append(resultX) if not (resultX == []) else (nucleiX.append(["NA"]))
        nucleiY.append(resultY) if not (resultY == []) else (nucleiY.append(["NA"]))
        nucleiZ.append(resultZ) if not (resultZ == []) else (nucleiZ.append(["NA"]))
        f.close()
    finalVol[i+1] = nucleiVol
    finalMinDist[i+1] = nucleiMinDist
    finalMaxDist[i+1] = nucleiMaxDist
    finalRatioDist[i+1] = nucleiRatioDist
    finalX[i+1] = nucleiX
    finalY[i+1] = nucleiY
    finalZ[i+1] = nucleiZ
    i += 1


if args.debug:
    replaceListSymbols = False

    f = open(os.path.join(path, "results-Volume-unfiltered.txt"), "w+")
    for entry in finalVol:
        if replaceListSymbols == False:
            f.write("{}\n".format(str(entry)))
        else:
            f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
    f.close()

    f = open(os.path.join(path, "results-MinDist-unfiltered.txt"), "w+")
    for entry in finalMinDist:
        if replaceListSymbols == False:
            f.write("{}\n".format(str(entry)))
        else:
            f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
    f.close()

    f = open(os.path.join(path, "results-MaxDist-unfiltered.txt"), "w+")
    for entry in finalMaxDist:
        if replaceListSymbols == False:
            f.write("{}\n".format(str(entry)))
        else:
            f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
    f.close()

    f = open(os.path.join(path, "results-RatioDist-unfiltered.txt"), "w+")
    for entry in finalRatioDist:
        if replaceListSymbols == False:
            f.write("{}\n".format(str(entry)))
        else:
            f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
    f.close()

    f = open(os.path.join(path, "results-X-unfiltered.txt"), "w+")
    for entry in finalX:
        if replaceListSymbols == False:
            f.write("{}\n".format(str(entry)))
        else:
            f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
    f.close()

    f = open(os.path.join(path, "results-Y-unfiltered.txt"), "w+")
    for entry in finalY:
        if replaceListSymbols == False:
            f.write("{}\n".format(str(entry)))
        else:
            f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
    f.close()

    f = open(os.path.join(path, "results-Z-unfiltered.txt"), "w+")
    for entry in finalZ:
        if replaceListSymbols == False:
            f.write("{}\n".format(str(entry)))
        else:
            f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
    f.close()

#### New filtering steps #####

##########################################
## Known bugs                           ##
##                                      ##
##                                      ##
##                                      ##
##                                      ##
##########################################

#Replace Timepoints with more than one hit with 'NA'
def removeDuplicates(*args):
    listCount = 1
    pointCount = 0 
    for lists in args:
        duplicatesRemovedTotal = 0
        for point in lists:
            uniquePoint = 0
            for time in point:
                if time == ['NA']:
                    pass            
                elif len(time) > 1:
                    if listCount == 1:
                        print("Point {}: Duplicate found".format(lists.index(point)))
                        print("Point {}: Duplicate found".format(lists.index(point)), file=log)
                        if uniquePoint == 0:
                            pointCount += 1  
                    lists[lists.index(point)][lists[lists.index(point)].index(time)] = ['NA']
                    duplicatesRemovedTotal += 1
                    uniquePoint += 1
                    
        listCount += 1
    print("Removed {} duplicates in total from {} points".format(duplicatesRemovedTotal, pointCount))
    print("Removed {} duplicates in total from {} points".format(duplicatesRemovedTotal, pointCount), file=log)

removeDuplicates(finalVol, finalMinDist, finalMaxDist, finalRatioDist, finalX, finalY, finalZ)
print("---------------------------------------------", file=log)

#Remove Spikes (Max-Min<2.5)
def removeSpikes(*args, ratioList):
    # get rid of the most nested list, because we excluded the possibility of duplicates with removeDuplicates()
    cleanList = []
    lookupList = []
    for point in ratioList:
        tempPointList = []
        tempLookupList = []
        for time in point:
            for item in time:
                if item != 'NA' and item != None:
                    tempPointList.append(item)
                    tempLookupList.append(item)
                else:
                    tempLookupList.append(item)
        cleanList.append(tempPointList)
        lookupList.append(tempLookupList)

    spikeCounter = 0
    spikePointsCounter = 0
    for cleanPoint in cleanList:
        if len(cleanPoint) != 0:
            difference = max(cleanPoint)-min(cleanPoint)
            pointSpikeCounter = 0
            while difference >= 2.5:
                if pointSpikeCounter == 0:
                    pointID = cleanList.index(cleanPoint)
                ratioList[cleanList.index(cleanPoint)][lookupList[cleanList.index(cleanPoint)].index(max(cleanPoint))] = ['NA']
                for lists in args:
                    lists[cleanList.index(cleanPoint)][lookupList[cleanList.index(cleanPoint)].index(max(cleanPoint))] = ['NA']
                cleanPoint.pop(cleanPoint.index(max(cleanPoint)))
                difference = max(cleanPoint)-min(cleanPoint)
                spikeCounter += 1
                pointSpikeCounter += 1
            if pointSpikeCounter != 0:
                print("Point {}: {} value(s) removed.".format(pointID, pointSpikeCounter))
                print("Point {}: {} value(s) removed.".format(pointID, pointSpikeCounter), file=log)
                spikePointsCounter += 1
        else:
            pass
    print("Removed {} spikes in {} points".format(spikeCounter, spikePointsCounter))
    print("Removed {} spikes in {} points".format(spikeCounter, spikePointsCounter), file=log)
    
# Remove Spikes is based on Ratio. It has to be passed as a keyworded argument or the function fails!
removeSpikes(finalVol, finalMinDist, finalMaxDist, finalX, finalY, finalZ, ratioList = finalRatioDist)
print("---------------------------------------------", file=log)

# Only display objects that are present in 80% of timepoints, replace others by text

def checkCoverage(*args):
    listCount = 1
    pointCount = 0
    for inputList in args:
        # get rid of the most nested list, because we excluded the possibility of duplicates with removeDuplicates()
        cleanList = []
        for point in inputList:
            tempPointList = []
            for time in point:
                for item in time:
                    tempPointList.append(item)
            cleanList.append(tempPointList)
        
        iterator = 0
        
        for point in cleanList:
            try:
                coverage = (len(point)-point.count('NA'))/len(point)
            except ZeroDivisionError:
                print("Coverage Calculation raised ZeroDivisonError on point {} for input-List number {}".format(iterator, listCount), file=log)
                iterator += 1
                continue
            if coverage < 0.7:
                if listCount == 1:
                    print("Point {} was only found in {}% of timepoints".format(iterator,round(coverage*100,2)))
                    print("Point {} was only found in {}% of timepoints".format(iterator,round(coverage*100,2)), file=log)
                    pointCount += 1
                #inputList[cleanList.index(point)] = "Coverage only {}%".format(coverage*100)
                inputList[iterator] = "Coverage_only_{}%".format(round(coverage*100,2))
            iterator += 1
        listCount += 1
    print("Replaced a total of {} points".format(pointCount))
    print("Replaced a total of {} points".format(pointCount), file=log)

checkCoverage(finalVol, finalMinDist, finalMaxDist, finalRatioDist, finalX, finalY, finalZ)
print("---------------------------------------------", file=log)
log.close()
print("Detection finished, writing results file")
    


replaceListSymbols = True 

f = open(os.path.join(path, "results-Volume.txt"), "w+")
for entry in finalVol:
    if replaceListSymbols == False:
        f.write("{}\n".format(str(entry)))
    else:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
f.close()

f = open(os.path.join(path, "results-MinDist.txt"), "w+")
for entry in finalMinDist:
    if replaceListSymbols == False:
        f.write("{}\n".format(str(entry)))
    else:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
f.close()

f = open(os.path.join(path, "results-MaxDist.txt"), "w+")
for entry in finalMaxDist:
    if replaceListSymbols == False:
        f.write("{}\n".format(str(entry)))
    else:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
f.close()

f = open(os.path.join(path, "results-RatioDist.txt"), "w+")
for entry in finalRatioDist:
    if replaceListSymbols == False:
        f.write("{}\n".format(str(entry)))
    else:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
f.close()

f = open(os.path.join(path, "results-X.txt"), "w+")
for entry in finalX:
    if replaceListSymbols == False:
        f.write("{}\n".format(str(entry)))
    else:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
f.close()

f = open(os.path.join(path, "results-Y.txt"), "w+")
for entry in finalY:
    if replaceListSymbols == False:
        f.write("{}\n".format(str(entry)))
    else:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
f.close()

f = open(os.path.join(path, "results-Z.txt"), "w+")
for entry in finalZ:
    if replaceListSymbols == False:
        f.write("{}\n".format(str(entry)))
    else:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
f.close()

print("Processing finished")
