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

from tensorflow import keras
from functools import partial
import tensorflow as tf
#import tensorflow as tf
#from tensorflow.keras.applications.resnet50 import ResNet50
# from tensorflow.keras 
# from tensorflow.keras.layers import Input, Flatten, Dense, Concatenate
#from keras import Input, Flatten, Dense, Concatenate
#from keras.models import Model
from keras.applications.resnet import ResNet50
from keras.layers import Input, Flatten, Dense, Concatenate
from keras.models import Model
from keras.optimizers import Adam
from keras.losses import BinaryCrossentropy
from keras.metrics import Accuracy
from keras.layers import LayerNormalization, MultiHeadAttention, Dropout, Dense, Layer
from keras.applications import VGG16
from keras.layers import Conv1D, Dense, MaxPool1D, GlobalAvgPool1D, Add, Activation, Input, Reshape
from keras.models import Model
#from tensorflow.keras.layers import Attention
from keras import layers


conv3 = partial(keras.layers.Conv1D, kernel_size=3, strides=1, padding='same', activation='relu')

def _block(in_layer, filters, n_convs):
  vgg_block = in_layer
  for _ in range(n_convs):
    vgg_block = conv3(filters=filters)(vgg_block)
  return vgg_block

def vgg(in_shape=(300,9)):
  in_layer = keras.layers.Input(in_shape)
  block1 = _block(in_layer, 64, 2)
  pool1 = keras.layers.MaxPool1D()(block1)
  block2 = _block(pool1, 128, 2)
  pool2 = keras.layers.MaxPool1D()(block2)
  block3 = _block(pool2, 256, 2)
  pool3 = keras.layers.MaxPool1D()(block3)
  block4 = _block(pool3, 512, 2)
  pool4 = keras.layers.MaxPool1D()(block4)
  block5 = _block(pool4, 512, 2)
  pool5 = keras.layers.MaxPool1D()(block5)
  flattened = keras.layers.GlobalAvgPool1D()(pool5)
  dense1 = keras.layers.Dense(2048, activation='relu')(flattened)
  dense2 = keras.layers.Dense(1024, activation='relu')(dense1)
  preds = keras.layers.Dense(1, activation='sigmoid')(dense2)
  model = keras.models.Model(in_layer, preds)
  model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model

def vgg_small(in_shape=(300, 6)):
  in_layer = keras.layers.Input(in_shape)
  block1 = _block(in_layer, 64, 2)
  pool1 = keras.layers.MaxPool1D()(block1)
  block2 = _block(pool1, 128, 2)
  pool2 = keras.layers.MaxPool1D()(block2)
  flattened = keras.layers.GlobalAvgPool1D()(pool2)
  dense1 = keras.layers.Dense(2048, activation='relu')(flattened)
  dense2 = keras.layers.Dense(1024, activation='relu')(dense1)
  preds = keras.layers.Dense(1, activation='sigmoid')(dense2)
  model = keras.models.Model(in_layer, preds)
  model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model 

def vgg_resnet(in_shape=(300, 9)):
    # VGG model
    in_layer = Input(in_shape)
    block1 = _block(in_layer, 64, 2)
    pool1 = keras.layers.MaxPool1D()(block1)
    block2 = _block(pool1, 128, 2)
    pool2 = keras.layers.MaxPool1D()(block2)
    block3 = _block(pool2, 256, 2)
    pool3 = keras.layers.MaxPool1D()(block3)
    block4 = _block(pool3, 512, 2)
    pool4 = keras.layers.MaxPool1D()(block4)
    block5 = _block(pool4, 512, 2)
    pool5 = keras.layers.MaxPool1D()(block5)
    flattened = keras.layers.GlobalAvgPool1D()(pool5)
    dense1 = keras.layers.Dense(2048, activation='relu')(flattened)
    
    # ResNet model
    resnet = ResNet50(weights='imagenet', include_top=False, input_shape=in_shape)
    resnet_output = resnet.output
    resnet_output = Flatten()(resnet_output)
    
    # Concatenate features
    merged_features = Concatenate()([dense1, resnet_output])
    
    dense2 = keras.layers.Dense(1024, activation='relu')(merged_features)
    preds = keras.layers.Dense(1, activation='sigmoid')(dense2)
    
    model = keras.models.Model(inputs=[in_layer, resnet.input], outputs=preds)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

def vgg_transformer(in_shape=(300, 9), embed_dim=256, num_heads=4, ff_dim=512):
    # VGG model
    vgg_model = VGG16(weights='imagenet', include_top=False, input_shape=in_shape)

    # Freeze VGG layers
    for layer in vgg_model.layers:
        layer.trainable = False

    # Flatten the output of VGG
    flatten = keras.layers.Flatten()(vgg_model.output)

    # Transformer input
    transformer_input = keras.layers.Reshape((300, 9))(flatten)

    # Transformer encoding
    transformer_output = TransformerEncoder(embed_dim, num_heads, ff_dim)(transformer_input)

    # Fully-connected layers
    dense1 = keras.layers.Dense(2048, activation='relu')(transformer_output)
    dense2 = keras.layers.Dense(1024, activation='relu')(dense1)

    # Output layer
    preds = keras.layers.Dense(1, activation='sigmoid')(dense2)

    # Create the model
    model = Model(inputs=vgg_model.input, outputs=preds)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


class TransformerEncoder(Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, rate=0.1):
        super(TransformerEncoder, self).__init__()
        self.att = MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim)
        self.ffn = keras.Sequential([Dense(ff_dim, activation="relu"), Dense(embed_dim),])
        self.layernorm1 = LayerNormalization(epsilon=1e-6)
        self.layernorm2 = LayerNormalization(epsilon=1e-6)
        self.dropout1 = Dropout(rate)
        self.dropout2 = Dropout(rate)

    def call(self, inputs, training=True):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn(out1)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)

# Create the combined model
#model = vgg_transformer()

# Print the model summary
#model.summary()
#上面的代码将VGG模型与Transformer编码器结合起来，形成了一个新的模型。VGG模型用于提取图像特征，然后通过Transformer编码器对特征进行进一步编码。最后，通过全连接层和输出层获得最终的预测结果。

class Attention(layers.Layer):
    def __init__(self, name=None, **kwargs):
        super(Attention, self).__init__(name=name, **kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name='attention_weight',
                                 shape=(input_shape[-1], 1),
                                 initializer='random_normal',
                                 trainable=True)
        self.b = self.add_weight(name='attention_bias',
                                 shape=(input_shape[-1],),
                                 initializer='zeros',
                                 trainable=True)

    def call(self, inputs):
        e = tf.matmul(inputs, self.W)
        e = layers.Activation('softmax')(e)
        output = tf.multiply(inputs, e)
        output = tf.reduce_sum(output, axis=1)
        output = tf.add(output, self.b)
        output = layers.Activation('tanh')(output)
        return output
    
def vgg_with_attention(in_shape=(300, 9)):
    in_layer = Input(in_shape)

    # VGG block 1
    conv1 = Conv1D(64, kernel_size=3, padding='same', activation='relu')(in_layer)
    conv1 = Conv1D(64, kernel_size=3, padding='same', activation='relu')(conv1)
    pool1 = MaxPool1D()(conv1)

    # VGG block 2
    conv2 = Conv1D(128, kernel_size=3, padding='same', activation='relu')(pool1)
    conv2 = Conv1D(128, kernel_size=3, padding='same', activation='relu')(conv2)
    pool2 = MaxPool1D()(conv2)

    # VGG block 3
    conv3 = Conv1D(256, kernel_size=3, padding='same', activation='relu')(pool2)
    conv3 = Conv1D(256, kernel_size=3, padding='same', activation='relu')(conv3)
    conv3 = Conv1D(256, kernel_size=3, padding='same', activation='relu')(conv3)
    pool3 = MaxPool1D()(conv3)

    # Self-Attention
    attn = Attention()(pool3)

    # Reshape for GlobalAvgPool1D
    reshape = Reshape((-1, 256))(attn)

    # Global average pooling
    flattened = GlobalAvgPool1D()(reshape)

    # Dense layers
    dense1 = Dense(2048, activation='relu')(flattened)
    dense2 = Dense(1024, activation='relu')(dense1)

    # Output layer
    preds = Dense(1, activation='sigmoid')(dense2)

    model = Model(inputs=in_layer, outputs=preds)
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model






