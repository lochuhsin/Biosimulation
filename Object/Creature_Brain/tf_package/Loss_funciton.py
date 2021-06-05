import tensorflow as tf

def cross_entropy(truth,prediction):
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(truth * tf.log(prediction),
                                              reduction_indices=[1])) 
    return cross_entropy