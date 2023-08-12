# Copyright (c) 2
##
# Licensed under 
# you may not use
# You may obtain 
##
# http://www.apac
##
# Unless required
# distributed und
# WITHOUT WARRANT
# See the License
# limitations und

#!/usr/bin/env py


import os
import sys

path = "F:\\XS\\prsms_zf1"
Filelist=os.listdir(path)
for File in Filelist:
    file=open("F:\\XS\\prsms_zf1\\"+File)
    all_lines = file.readlines()
    file.close()
    if len(all_lines) <= 2:
       #continue
       #spec_id=File.split('_')[-2]
       os.remove("F:\\XS\\prsms_zf1\\"+File)
       continue   #然后删除未被重命名的文件
    #filename = os.path.basename(File)
    for i in range(len(all_lines)):
       line = all_lines[i]
       mono = line.split('=')
    ## Reads Scan Number
       if("SPEC_ID" in line):
         spec_id = int(mono[1][0:len(mono[1])-1])
         break
    file_name ="F:\\XS\\prsms_zf1\\"+"sp_" + str(spec_id) + ".env"
    os.rename("F:\\XS\\prsms_zf1\\"+File, file_name)

















