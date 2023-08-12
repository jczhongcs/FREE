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
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import re
import numpy
from Data.feature_reader import read_feature_file
from Data.env_writer import write
from keras.models import load_model
import pathlib

#anno_dir = "D:\\envcnn-master\\src\\features"
anno_dir = "E:\\SXR2\\features5envcnn"

model_dir ="D:\\SXR\\envcnn-master\\src\\output"
#print(os.getcwd())
model = load_model('model.h5')
#model = load_model(os.path.join(model_dir, "model.h5"))

#files = [f for f in os.listdir(anno_dir) if re.match(r'feature*', f)]
files=list(pathlib.Path(anno_dir).glob('*.env'))
#files = [f for f in os.listdir(anno_dir) if re.match(r'.env', f)]
#files=os.listdir(anno_dir)
dir_name = "E:\\SXR2\\output_envs_zf5envcnn"
#ouput_dir = os.path.join(model_dir, dir_name)

if os.path.isdir(dir_name) == False:
  os.mkdir(dir_name)
	
for anno_file in files:
  env_list_with_features = read_feature_file(os.path.join(anno_dir, anno_file))
  for env in env_list_with_features:
    mat = env.getMatrix()
    #mat=mat.replace
    b = mat[numpy.newaxis,:, :]             #numpy.newaxi创建一个新轴，把原来的矩阵移到一行上，然后增加一列。
    #pred_score = model.predict(b)
    pred_score = model.predict(b)          
    env.header.pred_score = pred_score[0][0]  #得分是包络被归类成0的概率
  
  env_list_with_features.sort(key=lambda x: x.header.pred_score, reverse=True)  #reverse = True 降序
  output_file_name = os.path.join(dir_name, "Envelope_" + str(env.header.spec_id) + ".env")
  write(env_list_with_features, output_file_name)
