#os imported to read and manage flags directory
import os
from os import walk

#determine current working directory
workingdir = os.getcwd()

if workingdir[-3:] == "src":
    print("SOURCE Path:", workingdir)

else:
    workingdir = workingdir + "/src"
    print("SOURCE Path:", workingdir)

#establish path to flags
flagdir = workingdir + "/flags"
print("FLAGS  Path:", flagdir)

#ask os to list every file inside flag directory, remove any non -.png files
completeFlagList = next(walk(flagdir), (None, None, []))[2]

for flags in reversed(completeFlagList):
    if not(flags.endswith(".png")):
        completeFlagList.remove(flags)

print("Flags directory read, counted a total of", len(completeFlagList), "individual .png files.")
print()