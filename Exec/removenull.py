import os
import sys

path = "D:\\Env_data\\OT_mzML_data\\data2"
Filelist=os.listdir(path)
for File in Filelist:
    if ''in File:
        os.remove("D:\\Env_data\\OT_mzML_data\\data2\\"+File)