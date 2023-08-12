import os
import sys

file=os.listdir(r'D:\SXR\prsms')
for i in file:
    if "prsm" in i:
        os.remove(r'D:\SXR\prsms/'+i)









