#os imported to read and manage flags directory
import os
from os import walk

def flagImport(correctAmount):
    global workingdir
    global flagdir
    global completeFlagList

    #determine current working directory
    workingdir = os.getcwd()

    if workingdir[-3:] != "src":
        workingdir = workingdir + "/src"
    
    #add correct flag list to memory
    with open(workingdir + "/correctFlags.txt", 'r') as f:
        correctFlags = [line.strip() for line in f]

    #establish path to flags
    flagdir = workingdir + "/flags"

    #ask os to list every file inside flag directory, remove any non -.png files
    completeFlagList = next(walk(flagdir), (None, None, []))[2]

    for flags in reversed(completeFlagList):
        if not(flags.endswith(".png")):
            completeFlagList.remove(flags)

    completeFlagList.sort()

    #check if found flags match the correct flag list
    if completeFlagList != correctFlags or len(completeFlagList) != correctAmount:
        print()
        print("ERROR")
        print("Error while trying to ensure integrity of flag image source files.")

        if len(completeFlagList) != correctAmount:
            print(f"Found a total of {len(completeFlagList)} out of {correctAmount} .png files in {flagdir}.")
        
        print("Please see flags subdirectory within src directory to ensure every flag file is present and in .png format.")
        print("Software is trying to find a matching .png file for every 195 independent state listed at: https://www.worldometers.info/geography/how-many-countries-are-there-in-the-world/ and Taiwan, Western Sahara & Kosovo.")
    
    else:
        print("All 198 flags have been found.")

#debugging option
def listEverything():
    print("DEBUGGING:")
    print("SOURCE Path:", workingdir)
    print("FLAGS  Path:", flagdir)
    print("Amount of flags counted:", len(completeFlagList))
    print("Complete list:")

    completeFlagList.sort()

    for flags in completeFlagList:
        print(flags)

flagImport(198)