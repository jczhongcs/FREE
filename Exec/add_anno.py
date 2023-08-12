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
from Data.env_reader import read_env_file
from Data.prsm_reader import read_prsm_file
from Data.env_writer import write as env_writer
import Data.env_util as env_util


#prsm_file  =  open('D:\\Env_data\\prsms')
path="E:\\SXR2\\prsms_zf5"
Filelist=os.listdir(path)
for prsm_file in Filelist:
 start = prsm_file.index('_') + 1
 end = prsm_file.index( '.', start )
 index = prsm_file[start:end]
 output_file  =  "E:\\SXR2\\annotated5\\"+"annotated_" + prsm_file[start:end] + ".env"
 prsm = read_prsm_file("E:\\SXR2\\prsms_zf5\\"+prsm_file)  #为蛋白质数据库中的每种蛋白质生成了一份理论上的N端离子单同位素质量列表,若该质谱有匹配的蛋白质序列则装入prsm文件夹中，可以得到Prsm(spec_id, prot_seq, peak_list, acetylation)
 if prsm is None:
  exit()

 path="E:\\SXR\\ZF5"
 env_file=path+"\\"+"sp_"+index+".env"
 env_list = read_env_file(env_file)
 prsm.annotate(env_list)        #先得到toppic计算出的同位素峰值质量，以及头文件中得到的理论质量,当精度等于15*碎片质量/1000000时且env的头文件的离子类型为空时，则添加离子类型
                                  #每一个prsm可以得到14种理论碎片质量，当得到符合条件的离子质量时，将env.header.ion_type中的离子类型改成相应的离子
 for env in env_list:
   env_util.assign_labels(env)   #当出现B离子或者是Y离子时，将env.header.label置为1
   env.get_intv_peak_list()

   env_writer(env_list, output_file)
