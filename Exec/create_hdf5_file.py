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
import h5py
import Data.train_model_util as util
import Data.hdf5_util as h5_util

#path="D:\\envcnn-master\\src\\traindata\\"
path="E:\\SXR2\\TrainData6\\"
#path="D:\\SXR\\TrainData\\"
#Filelist=os.listdir(path)
#for data_dir in Filelist:
  #print(data_dir)               
params_dict = util.get_param_dict(path) ## Read params_dict
labels_dict = util.get_label_dict(path) ## Read labels file
util.shortlist_dictionaries(params_dict, labels_dict) ## removes all annotations other than B and Y.如果离子不是b/y离子，则在label.csv和parameters.csv文件里删除它们所在的行
data_files, labels = util.shuffle_data(labels_dict)   #打乱数据
train_data_files, validation_data_files, test_data_files, train_labels, validation_labels, test_labels = util.split_data_single_2(data_files, labels)
#print("finished")
hdf5_path = "E:\\SXR2\\dataset_zf6.hdf5"
hdf5_file = h5py.File(hdf5_path, mode='a') 
h5_util.write_hdf5_categories(300, 9, hdf5_file, train_data_files, validation_data_files, test_data_files)
h5_util.write_labels(hdf5_file, train_labels, validation_labels, test_labels)
h5_util.write_params(hdf5_file, params_dict, train_data_files, validation_data_files, test_data_files)
h5_util.write_train_matrix(hdf5_file, train_data_files, path)
h5_util.write_val_matrix(hdf5_file, validation_data_files, path)
h5_util.write_test_matrix(hdf5_file, test_data_files, path)
hdf5_file.close()
