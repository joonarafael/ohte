#os imported to read and manage flags directory
import os
from os import walk

#determine current working directory
workingdir = os.getcwd()

if workingdir[-3:] != "src":
    workingdir = workingdir + "/src"

#establish path to flags
flagdir = workingdir + "/flags"

#ask os to list every file inside flag directory, remove any non -.png files
completeFlagList = next(walk(flagdir), (None, None, []))[2]

for flags in reversed(completeFlagList):
    if not(flags.endswith(".png")):
        completeFlagList.remove(flags)

if len(completeFlagList) != 200:
    print("Tried to read flags source files (.png images), counted a total of", len(completeFlagList), ".")
    print("This is not the correct amount of files on disk. Please see flags subdirectory within src directory to ensure every flag file is present and in .png format.")

def listEverything():
    print()
    print("DEBUGGING:")
    print("SOURCE Path:", workingdir)
    print("FLAGS  Path:", flagdir)
    print("Amount of flags counted:", len(completeFlagList))
    print("Complete list:")

    completeFlagList.sort()

    for flags in completeFlagList:
        print(flags)