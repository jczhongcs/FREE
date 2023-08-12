import sys
import os
path =os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)
from Data.env_reader import read_env_file
from Data.prsm_reader import read_prsm_file
from Data.env_writer import write as env_writer
import Data.env_util as env_util
import matplotlib.pyplot as plt

tolerance = 0.02
path="E:\\SXR\\annotated1\\annotated_332.env"
env_list = read_env_file(path)
X=[]
Y=[]
for env in env_list:
    for peak in env.exp_peak_list:
        X.append(peak.mass)
        Y.append(peak.intensity)
plt.figure(figsize=(8,6))  # 定义图的大小
plt.xlabel("m/z values")     # X轴标签
plt.ylabel("Intensities")        # Y轴坐标标签
plt.title("Original data")      #  曲线图的标题

plt.plot(X,Y)            # 绘制曲线图
#在ipython的交互环境中需要这句话才能显示出来
plt.show()
