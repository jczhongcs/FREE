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

import os
import sys
path =os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)
from Data.feature_reader import read_feature_file
from Data.matrix_writer import write as matrix_writer
#path="C:\\Users\宋星燃\\Desktop\\features\\"
path="E:\\SXR2\\features6\\"
Filelist=os.listdir(path)

for feature_file in Filelist:
  file_prefix ="E:\\SXR2\\TrainData6\\"+"features"
  env_list_with_features = read_feature_file(path+feature_file)
  print(os.getcwd())
  for env in env_list_with_features:
    mat = env.getMatrix()
    matrix_writer(env, mat, file_prefix)
