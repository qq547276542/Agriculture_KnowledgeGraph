import tensorflow as tf

def softmax_cross_entropy(x,label,rel_tot,weights_table = None,var_scope = None):
    with tf.variable_scope("loss",reuse = tf.AUTO_REUSE):
        if weights_table is None:
            weights = 1.0

        else:
            weights = tf.nn.embedding_lookup(weights_table,label)

        label_onehot = tf.one_hot(indices=label,depth=rel_tot,dtype=tf.int32)
        loss = tf.losses.softmax_cross_entropy(onehot_labels=label_onehot,logits=x,weights = weights)
        tf.summary.scalar('loss',loss)
        return loss