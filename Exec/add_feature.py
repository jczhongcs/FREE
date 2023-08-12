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
path =os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)
import Data.env_util as env_util
from Data.anno_reader import read_anno_file
from Data.feature_writer import write as feature_writer

tolerance = 0.02
path="E:\\SXR2\\annotated4envcnn\\"
Filelist=os.listdir(path)
for anno_file in Filelist:
  output_file  = "E:\\SXR2\\features4envcnn\\" +"feature"+ anno_file[anno_file.rindex("_"):anno_file.rindex(".")] + ".env"
  env_list = read_anno_file(path+anno_file)
  for idx in range(len(env_list)):
   env = env_list[idx]
   env.get_peak_feature_list(tolerance)  
   feature_writer(env_list, output_file)
