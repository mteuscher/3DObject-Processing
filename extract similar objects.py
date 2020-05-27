import os
import sys

X = []
Y = []
Z = []


path = str(input("Enter Path:"))
file_type = str(input("Enter file suffix:"))
name_part = str(input("Only Process files containing:"))
referenceTimepoint = int(input("Which Timepoint to use as Reference?:"))


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
                    print("Provided suffix is not a string")
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
            for directory, dir_names, file_names in os.walk(folder):
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
    if line.split(sep="\t")[10] is not "X":
        if X_temp-5 < float(line.split(sep="\t")[10]) < X_temp+5:
            if Y_temp-5 < float(line.split(sep="\t")[11]) < Y_temp+5:
                if Z_temp-5 < float(line.split(sep="\t")[12]) < Z_temp+5:
                    lineVol = float(line.split(sep="\t")[0])
                    lineX = float(line.split(sep="\t")[10])
                    lineY = float(line.split(sep="\t")[11])
                    lineZ = float(line.split(sep="\t")[12])
                    return lineVol, lineX, lineY, lineZ
    
def analyzeFile(filename):    
    foundValue = []
    with open(openFile) as f:
        for line in f:
            temp = process(line)
            if temp is not None:
                foundValue.append(temp)
    f.close()
    return foundValue

files = generateFileList(path, file_type, name_part)

f = open(str(files[referenceTimepoint-1]))
for line in f:
    if line.split(sep="\t")[10] is not "X":
        X.append(float(line.split(sep="\t")[10]))
        Y.append(float(line.split(sep="\t")[11]))
        Z.append(float(line.split(sep="\t")[12]))
f.close()

finalVol = []
finalX = []
finalY = []
finalZ = []

header = []
for file in files:
    header.append(file.split(os.sep)[-1])
    
finalVol.append(header)
finalX.append(header)
finalY.append(header)
finalZ.append(header)



for entry in X:
    finalVol.append("NA")
    finalX.append("NA")
    finalY.append("NA")
    finalZ.append("NA")

print("Detected {} files for Processing".format(len(files)))
if query_yes_no("Do you want to inspect the files and their order?") is True:
    for file in files:
        print(file)
    
print("\nYour reference Timepoint is the file: {}\nIt contains {} objects".format(str(files[referenceTimepoint-1]), len(X)))
if query_yes_no("Do you want to continue?") is False:
    sys.exit()


i=0
while i < len(X):
    X_temp = X[i]
    Y_temp = Y[i]
    Z_temp = Z[i]
    nucleiVol = []
    nucleiX = []
    nucleiY = []
    nucleiZ = []
    
    os.system('cls')
    print("Processing value {}/{}".format(i+1,len(X)))
    
    for file in files:
        #result = ["TP{}".format(sortNames(file))]
        resultVol, resultX, resultY, resultZ = [], [], [], []

        f = open(str(file))
        for line in f:
            temp = process(line)
            if temp is not None:
                resultVol.append(temp[0])
                resultX.append(temp[1])
                resultY.append(temp[2])
                resultZ.append(temp[3])
        nucleiVol.append(resultVol) if not (resultVol == []) else (nucleiVol.append("NA"))
        nucleiX.append(resultX) if not (resultX == []) else (nucleiX.append("NA"))
        nucleiY.append(resultY) if not (resultY == []) else (nucleiY.append("NA"))
        nucleiZ.append(resultZ) if not (resultZ == []) else (nucleiZ.append("NA"))
        f.close()
    finalVol[i+1] = nucleiVol
    finalX[i+1] = nucleiX
    finalY[i+1] = nucleiY
    finalZ[i+1] = nucleiZ
    i += 1

print("Detection finished, writing results file")
    
f = open(os.path.join(path, "results-Volume-Reference_{}.csv".format(str(files[referenceTimepoint-1]).split(os.sep)[-1])), "w+")
j = 0
for entry in finalVol:
    if j == 0:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","")))
    else:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
    j += 1
f.close()

f = open(os.path.join(path, "results-X-Reference_{}.csv".format(str(files[referenceTimepoint-1]).split(os.sep)[-1])), "w+")
j = 0
for entry in finalX:
    if j == 0:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","")))
    else:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
    j += 1
f.close()

f = open(os.path.join(path, "results-Y-Reference_{}.csv".format(str(files[referenceTimepoint-1]).split(os.sep)[-1])), "w+")
j = 0
for entry in finalY:
    if j == 0:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","")))
    else:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
    j += 1
f.close()

f = open(os.path.join(path, "results-Z-Reference_{}.csv".format(str(files[referenceTimepoint-1]).split(os.sep)[-1])), "w+")
j = 0
for entry in finalZ:
    if j == 0:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","")))
    else:
        f.write("{}\n".format(str(entry).replace("[","").replace("]","").replace("\'","").replace(" ","")))
    j += 1
f.close()

print("Processing finished")
