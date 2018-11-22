import sys
sys.path.append("..")
import config
import tensorflow as tf
import numpy as np

def __cnn_cell__(x,hidden_size,kernel_size,stride_size):
    x = tf.layers.conv1d(inputs=x,
                         filters = hidden_size,
                         kernel_size=kernel_size,
                         strides = stride_size,
                         padding = 'same',
                         kernel_initializer=tf.contrib.layers.xavier_initializer())
    return x

def __dropout__(x,keep_prob= 1.0):
    return tf.contrib.layers.dropout(x,keep_prob=keep_prob)

def __piecewise_pooling(x,mask):
    mask_embedding = tf.constant([[0,0,0],[1,0,0],[0,1,0],[0,0,1]],dtype = np.float32)
    mask = tf.nn.embedding_lookup(mask_embedding,mask)
    hidden_size = x.shape[-1]

    x = tf.reduce_max(tf.expand_dims(mask*1000,2) + tf.expand_dims(x,3) , axis=1) - 1000

    return tf.reshape(x,[-1,hidden_size*3])


def pcnn(x,mask,keep_prob,hidden_size= config.model.pcnn_hidden_size,kernel_size = config.model.pcnn_kernel_size,stride_size = config.model.pcnn_stride_size,
         activation=config.model.pcnn_activation,var_scope=None):
    with tf.variable_scope("pcnn", reuse = tf.AUTO_REUSE):
        x = __cnn_cell__(x,hidden_size,kernel_size,stride_size)
        x = __piecewise_pooling(x,mask)
        x = activation(x)
        x = __dropout__(x,keep_prob=keep_prob)

        return x



