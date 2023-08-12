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
import numpy
import math
import Data.env_util as EnvUtil
from Data.feature import Feature

class Envelope:
  def __init__(self, header, theo_peak_list, exp_peak_list, min_exp_mz, feature_list):
    self.header = header
    self.theo_peak_list = theo_peak_list
    self.exp_peak_list = exp_peak_list
    self.min_exp_mz = min_exp_mz
    self.feature_list = feature_list
    # self.intv_peak_list = intv_peak_list

  @classmethod
  def get_env(cls, header, theo_peak_list, exp_peak_list):
    min_exp_mz = ""
    feature = ""
    return cls(header, theo_peak_list, exp_peak_list, min_exp_mz, feature)

  def get_intv_peak_list(self):
    intv_peak_list = []
    min_theo_peak = min(self.theo_peak_list, key=lambda x: x.mass).mass
    max_theo_peak = max(self.theo_peak_list, key=lambda x: x.mass).mass
    for peak in self.exp_peak_list:
      if ((peak.mass >= min_theo_peak - 0.1) and (peak.mass <= max_theo_peak + 0.1)):
        intv_peak_list.append(peak)
    self.exp_peak_list = intv_peak_list

  def get_peak_feature_list(self, tolerance):
    feature_list = []
    self.min_exp_mz = self.header.mono_mz - 0.1
    ## get the max_theo_inetensity and Normalize the intensities
    max_theo_intensity = EnvUtil.get_max_intensity(self.theo_peak_list)
    log_theo_intensity = math.log10(max_theo_intensity)
    log_base_intenisty = math.log10(self.header.base_inte)
    charge = self.header.charge
    inte_dot_proc=self.header.inte_dot_proc
    inte_os_dis=self.header.inte_os_dis
    inte_mhd_dis=self.header.inte_mhd_dis
    inte_qbxf_dis=self.header.inte_qbxf_dis
    inte_nom_os_dis=self.header.inte_nom_os_dis
    # inte_dot_proc=self.header.inte_dot_proc
    for peak in self.theo_peak_list:
      bin_index = EnvUtil.get_bin_indx(peak.mass, self.min_exp_mz)
      norm_theo_peak_inte = EnvUtil.get_normalized_intensity(peak.intensity, max_theo_intensity)
      exp_peak_idx = EnvUtil.find_exp_peak_idx(peak, self.exp_peak_list, tolerance)
      if exp_peak_idx >= 0:
        exp_peak = self.exp_peak_list[exp_peak_idx]
        norm_exp_peak_inte = EnvUtil.get_normalized_intensity(exp_peak.intensity, max_theo_intensity)
        mass_diff = peak.mass - exp_peak.mass
        inte_diff = norm_theo_peak_inte - norm_exp_peak_inte
      else:
        norm_exp_peak_inte = 0
        mass_diff = -peak.mass
        inte_diff = norm_theo_peak_inte - norm_exp_peak_inte
      feature = Feature(bin_index, norm_theo_peak_inte, norm_exp_peak_inte, charge, 
                            mass_diff, inte_diff, log_theo_intensity, log_base_intenisty, inte_dot_proc, inte_os_dis, inte_mhd_dis,inte_qbxf_dis,inte_nom_os_dis)
      feature_list.append(feature)
    self.feature_list = feature_list

  def getMatrix(self):
    matrix = numpy.zeros(shape=(300, 9))
    max_theo_intensity = EnvUtil.get_max_intensity(self.theo_peak_list)
    for feature in self.feature_list:
      EnvUtil.populate_matrix(feature, matrix, self.header.mono_mass) #对于每一行（一组）特征的值，创建一个矩阵
      
    for peak in self.exp_peak_list:
      pos = EnvUtil.get_bin_indx(peak.mass, self.min_exp_mz)
      ## Evaluate Peak Condition
      peak_condition = False
      for i in range(0, 3):
	  ## to accomodate +2 and -2 bins - reason tolerance of 0.02. We have already selected the best peak - with min mass_diff
        if pos + i < 300 and pos - i > -1 and matrix[pos][0] == 0:  #只有峰值mz值在0-299内才会被收录，且第一行为零
          if matrix[pos - i][0] == 0 and matrix[pos + i][0] == 0:   #且与pos相邻为i（0<=i<2）的bin的第一行的值都为0
            peak_condition = True
          else:
            peak_condition = False
            break
      ## populate noise peaks
      if peak_condition == True:
        matrix[pos][1] = EnvUtil.get_normalized_intensity(peak.intensity, max_theo_intensity)  #因为每个bin相差为0.01，如果该pos所位于的bin的相邻两个bin中都没有峰
    return matrix
