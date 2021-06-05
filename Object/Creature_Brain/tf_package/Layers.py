import tensorflow as tf


def Dense_layer(inputs,n_units,activation = None,):
    dense = tf.layers.Dense(units=n_units,activation=tf.nn.relu,
                            kernel_initializer=tf.initializers.random_normal,
                            bias_initializer=tf.initializers.random_normal) 
    output = dense(inputs = inputs)
    return output



def Conv2d_layer(inputs,filters = 32,kernal_size = 5,activation = None):
    conv2d = tf.layers.Conv2D(filters=filters,    ### this creates a conv2d class and returns a tensor immediatly
                              kernel_size=kernal_size, activation=tf.nn.relu,
                              kernel_initializer=tf.initializers.random_normal,
                              bias_initializer=tf.initializers.random_normal) 
    output = conv2d(inputs=inputs)
    return output



def Dropout(inputs):
    dropout = tf.layers.Dropout()
    output = dropout(inputs)
    
    return output



### used to connect between convolute layer and Dense 
def Flatten(inputs):
    flatten = tf.layers.Flatten()
    output = flatten(inputs)
    return output