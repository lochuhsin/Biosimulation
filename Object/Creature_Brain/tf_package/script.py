import Layers as layers
import Loss_funciton as loss
import Utility
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("/tmp/data/", one_hot=True)

def compute_accuracy(v_xs, v_ys):
    global prediction
    y_pre = sess.run(output4, feed_dict={x: v_xs, })
    correct_prediction = tf.equal(tf.argmax(y_pre,1), tf.argmax(v_ys,1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    result = sess.run(accuracy, feed_dict={x: v_xs, y_: v_ys, })

    return result



x = tf.placeholder(tf.float32,shape=[None,784])
y_ = tf.placeholder(tf.float32,shape=[None,10])

inputs = tf.reshape(x ,[-1,28,28,1])


### construct layers
output1 = layers.Conv2d_layer(inputs)
output2 = layers.Conv2d_layer(output1)
output3 = layers.Flatten(output2)
output4 = layers.Dense_layer(output3,10)

cross_entropy = loss.cross_entropy(y_,output4)

optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(cross_entropy)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)


for i in range(10000):
    batch_x,batch_y = mnist.train.next_batch(100)
    sess.run(fetches=train,feed_dict={x : batch_x,y_ : batch_y})
    
    if i % 200 == 0:
        print(compute_accuracy(
            mnist.test.images[:1000], mnist.test.labels[:1000]))