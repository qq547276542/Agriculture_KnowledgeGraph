import tensorflow as tf
def __dropout__(x,keep_prob= 1.0):
    return tf.contrib.layers.dropout(x,keep_prob=keep_prob)

def __logit__(x,rel_tot):
    with tf.variable_scope('logit',reuse = tf.AUTO_REUSE):
        relation_matrix = tf.get_variable('relation_matrix',shape=[rel_tot,x.shape[1]],dtype=tf.float32,initializer=tf.contrib.layers.xavier_initializer())
        bias = tf.get_variable('bias',shape=[rel_tot],dtype=tf.float32,initializer=tf.contrib.layers.xavier_initializer())
        logit = tf.matmul(x,tf.transpose(relation_matrix)) + bias

    return logit

def bag_average(x,scope,rel_tot,var_scope=None,dropout_before = False,keep_prob= 1.0):
    with tf.variable_scope("average",reuse=tf.AUTO_REUSE):
        if dropout_before:
            x = __dropout__(x,keep_prob)
        bag_repre = []
        for i in range(scope.shape[0]):
            bag_hidden_mat = x[scope[i][0]:scope[i][1]]
            bag_repre.append(tf.reduce_mean(bag_hidden_mat,0))

        bag_repre = tf.stack(bag_repre)
        if not dropout_before:
            bag_repre = __dropout__(bag_repre,keep_prob)

    return __logit__(bag_repre,rel_tot) , bag_repre