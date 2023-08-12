##Copyright (c) 2014 - 2020, The Trustees of Indiana University.
##
##Licensed under the Apache License, Version 2.0 (the "License");
##you may not use this file except in compliance with the License.
##You may obtain a copy of the License at
##
##    http://www.apache.org/licenses/LICENSE-2.0
##
##Unless required by applicable law or agreed to in writing, software
##distributed under the License is distributed on an "AS IS" BASIS,
##WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##See the License for the specific language governing permissions and
##limitations under the License.

#!/usr/bin/env python3

import sys
import os
import xml.etree.ElementTree as ET
from shutil import copyfile
import glob
path = "E:\\SXR2\\prsms_zf5"
Filelist=os.listdir(path)
for File in Filelist:
    file=open("E:\\SXR2\\prsms_zf5\\"+File)
    all_lines = file.readlines()
    file.close()
    #filename = os.path.basename(File)
    if len(all_lines) < 2:
      exit()
    for i in range(len(all_lines)):
       line = all_lines[i]
       mono = line.split('=')
  ## Reads Scan Number
       if("spec_id" in line):
         mono=line.split('>')
         index=mono[1].index('<')
         spec_id = int(mono[1][0:index])
         file_name ="E:\\SXR2\\prsms_zf5\\"+"sp_" + str(spec_id) + ".xml"
         os.rename("E:\\SXR2\\prsms_zf5\\"+File, file_name)
         break