import os
from os import walk

workingdir = os.getcwd()
print("SRC Path:", workingdir)

flagdir = workingdir + "/flags"
print("Flags Path:", flagdir)

completeFlagList = next(walk(flagdir), (None, None, []))[2]
print("Flags read, counted a total of", len(completeFlagList), "flags.")