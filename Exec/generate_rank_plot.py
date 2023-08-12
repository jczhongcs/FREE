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
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

anno_dir1 = "E:\\SXR2\\output_envs_zf6"
anno_dir2="E:\\SXR2\\output_envs_zf6envcnn"
files = os.listdir(anno_dir1)
#将包络根据topfd得分和envcnn得分排名
env_list_2d_topfd = []
#env_list_2d_pred_score = []
for anno_file in files:
  env_list = read_anno_file(os.path.join(anno_dir1, anno_file))
  ## Rank by TopFD score
  env_list.sort(key=lambda x: x.header.topfd_score, reverse=True) #key 主要是用来进行比较的元素，reverse = True 降序
  env_list_2d_topfd.append(env_list)
  ## Rank by EnvCNN prediction score  
  #env_list.sort(key=lambda x: x.header.pred_score, reverse=True)
  #env_list_2d_pred_score.append(env_list)
env_list_2d_pred_score1 = []
for anno_file in files:
  env_list = read_anno_file(os.path.join(anno_dir1, anno_file))
  env_list.sort(key=lambda x: x.header.pred_score, reverse=True)
  env_list_2d_pred_score1.append(env_list)

env_list_2d_pred_score2 = []
for anno_file in files:
  env_list = read_anno_file(os.path.join(anno_dir2, anno_file))
  env_list.sort(key=lambda x: x.header.pred_score, reverse=True)
  env_list_2d_pred_score2.append(env_list)

## Computing Ranks TopFD
rank_len = 500

b_list_topfd = [0] * rank_len
y_list_topfd = [0] * rank_len
for i in range(len(env_list_2d_topfd)):
  for j in range(len(env_list_2d_topfd[i])):
    if j >= rank_len:
      break
    if env_list_2d_topfd[i][j].header.ion_type == "B":#env_list_2d_topfd[i][j]代表每一个.env文件中的每一个包络，每一个.env文件中的包络是按分数排名的，统计每一个排名下的正包络的数目（即纵坐标prsms的数目）
      b_list_topfd[j] = b_list_topfd[j] + 1
    if env_list_2d_topfd[i][j].header.ion_type == "Y":
      y_list_topfd[j] = y_list_topfd[j] + 1     #对于得分排名前500包络，如果匹配的离子是b或y离子（为正包络的话），计算其是b或y离子匹配中的包络之间的排名

## Computing Ranks Pred_Score
rank_len = 500
b_list_pred_score1 = [0] * rank_len
y_list_pred_score1 = [0] * rank_len
for i in range(len(env_list_2d_pred_score1)):
  #print("env_list", i)
  for j in range(len(env_list_2d_pred_score1[i])):
    if j >= rank_len:
      break
    if env_list_2d_pred_score1[i][j].header.ion_type == "B":
      b_list_pred_score1[j] = b_list_pred_score1[j] + 1     #b_list_pred_score记录了所有.env文件中，每个排名上与b离子质量匹配的包络（即正包络）
    if env_list_2d_pred_score1[i][j].header.ion_type == "Y":
      y_list_pred_score1[j] = y_list_pred_score1[j] + 1

rank_len = 500
b_list_pred_score2 = [0] * rank_len
y_list_pred_score2 = [0] * rank_len
for i in range(len(env_list_2d_pred_score2)):
  #print("env_list", i)
  for j in range(len(env_list_2d_pred_score2[i])):
    if j >= rank_len:
      break
    if env_list_2d_pred_score2[i][j].header.ion_type == "B":
      b_list_pred_score2[j] = b_list_pred_score2[j] + 1     #b_list_pred_score记录了所有.env文件中，每个排名上与b离子质量匹配的包络（即正包络）
    if env_list_2d_pred_score2[i][j].header.ion_type == "Y":
      y_list_pred_score2[j] = y_list_pred_score2[j] + 1
## Computing percentage
length = 100
pred_score_percentage_envcnn = [0] * length
#topFD_percentage = [0] * length
for i in range(length):
  pred_score_percentage_envcnn[i] = (b_list_pred_score1[i]+y_list_pred_score1[i])#对于
  #topFD_percentage[i] = (b_list_topfd[i]+y_list_topfd[i])
pred_score_percentage_me = [0] * length
#topFD_percentage = [0] * length
for i in range(length):
  pred_score_percentage_me[i] = (b_list_pred_score2[i]+y_list_pred_score2[i])#对于

topFD_percentage = [0] * length
for i in range(length):
  topFD_percentage[i] = (b_list_topfd[i]+y_list_topfd[i])
## Plotting Graph  
graph_file_name = os.path.join(os.getcwd(), "Rank.png")#根据envcnn_score和topfd_score对包络进行排名。对于每个.env文件中前500个包络，如果其与b离子或y离子匹配，则将b,y离子列表内排名为1，统计有哪些.env文件中位于第1位置的包络是正包络（即看位于第一的这个包络的匹配离子类型是否是b或y离子）
plt.figure()

plt.plot(list(range(0, length)), pred_score_percentage_envcnn)
plt.plot(list(range(0, length)), pred_score_percentage_me)
plt.plot(list(range(0, length)), topFD_percentage)
plt.title('Rank Plot')
plt.ylabel('Number of PrSMs with label 1')
plt.xlabel('Rank Number')
plt.legend(['EFRIEE','EnvCNN', 'TopFD'], loc='upper right')
plt.savefig(graph_file_name, dpi=500)
plt.close()
