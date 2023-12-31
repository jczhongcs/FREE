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

import sys
import os
path =os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)
import keras
import h5py
import numpy
from sklearn.metrics import balanced_accuracy_score
from keras.models import load_model
import Data.train_model_util as train_model_util
import Data.test_model_util as test_model_util
import math

data_dir = "E:\\SXR2\\dataset_zf5.hdf5" ## HDF5 file
output_dir = "D:\\SXR\\envcnn-master\\src\\output" ## contains Model
hdf5_file = h5py.File(data_dir, "r")
x_train = hdf5_file['test_data'][:,:,0:9]
y_train = hdf5_file['test_labels']
z_train = hdf5_file['test_params']

### Plot labels distribution
#test_model_util.get_anno_dist(output_dir, x_train, y_train, z_train)

## Accuracy and Loss for Charge states
x_train1 = numpy.stack(list(x_train))
y_train= numpy.array(list(y_train))
#test_model_util.get_label_distribution(output_dir, x_train, y_train)

## Evaluate model performance on test data
model = load_model(os.path.join(output_dir, "model.h5"))
model.compile(loss = "binary_crossentropy", metrics=['accuracy'], optimizer=keras.optimizers.Adam())
history = model.evaluate(x_train, y_train, verbose=0)
predictions = model.predict(x_train, verbose=0)

predictions_labels= [round(x[0]) for x in predictions]
balanced_accuracy = balanced_accuracy_score(y_train, predictions_labels, adjusted=False)

C = confusion_matrix(y_train, predictions_labels)
print(C)
res=0
sum=0
res=C[0][0]+C[1][1]
sum=res+C[0][1]+C[1][0]
#print(sum(C))
accuracy_value=res/sum 


tp=0
tp=C[1][1]
fn=0
fn=C[0][1]
fp=0
fp=C[1][0]
precison=0
recall=0
precision=tp/(tp+fp)
recall=tp/(tp+fn)
F_score=2*precision*recall/(precision+recall)

print("** Overall Performance **")
#print("Loss:", history[0], "Accuracy:", history[1])
print("Accuracy:", accuracy_value)
print("Balanced Accuracy:", balanced_accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F_score:", F_score)
#test_model_util.generate_roc_curve(output_dir, predictions, y_train, file_name="ROC_Curve_Test.png")
test_model_util.generate_roc_curve_test(output_dir, predictions, y_train, file_name="ROC_Curve_Test.png")

