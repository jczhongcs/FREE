import sys
import os
path =os.path.dirname(os.path.dirname(__file__))
sys.path.append(path)
#os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
import keras
import math
import h5py
import Data.models as models
from keras.models import load_model
#model_dir = "D:\\SXR\\envcnn-master\\src\\output"
#model = load_model(os.path.join(model_dir, "model.h5"))
model = load_model("modeldotosmhdqbxf.h5")
#model = models.vgg()
model.summary()

