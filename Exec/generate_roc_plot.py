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

#!/usr/bin/python3

import os
import sys
path =os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)
from Data.anno_reader import read_anno_file
import Data.test_model_util as test_model_util 
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np

anno_dir1 = "E:\\SXR2\\output_envs_zf6envcnn"
files1= os.listdir(anno_dir1)
anno_dir2 = "E:\\SXR2\\output_envs_zf6"
files2= os.listdir(anno_dir2)

labels_envcnn = []
labels_me = []
pred_score_envcnn = []
pred_score_me = []
topfd_score = []
for anno_file in files1:
  env_list = read_anno_file(os.path.join(anno_dir1, anno_file))
  env_label_envcnn = []
  env_pred_score_envcnn = []
  env_pred_score_me = []
  env_topfd_score = []
  for env in env_list:
    env_label_envcnn.append(env.header.label)
    env_pred_score_envcnn.append(env.header.pred_score)

    env_topfd_score.append(env.header.topfd_score)


  max_topfd_score = max(env_topfd_score)
  if max_topfd_score > 0:
    normalized_env_topfd_score = [x / max_topfd_score for x in env_topfd_score]
  else:
    normalized_env_topfd_score =  env_topfd_score
  labels_envcnn.extend(env_label_envcnn)
  pred_score_envcnn.extend(env_pred_score_envcnn)  
  topfd_score.extend(normalized_env_topfd_score)
for anno_file in files2:
  env_label_me = []
  env_list = read_anno_file(os.path.join(anno_dir2, anno_file))
  env_pred_score_me = []
  for env in env_list:
    env_label_me.append(env.header.label)
    env_pred_score_me.append(env.header.pred_score)
  labels_me.extend(env_label_me)
  pred_score_me.extend(env_pred_score_me)
  
pred_score_envcnn=np.nan_to_num(pred_score_envcnn, nan=0.0)
pred_score_me= np.nan_to_num(pred_score_me, nan=0.0)
print(np.isnan(pred_score_envcnn).any())
print(np.isnan(pred_score_me).any())
test_model_util.generate_roc_curve(os.getcwd(), pred_score_me, pred_score_envcnn, topfd_score, labels_envcnn,labels_me)
