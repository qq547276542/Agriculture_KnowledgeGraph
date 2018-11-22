import sys
import tensorflow as tf
sys.path.append("..")
import config
import numpy as np

def word_embedding(word,word_vec_mat,var_scope,word_embedding_dim,add_unk_blank):
    with tf.variable_scope('word_embedding',reuse = tf.AUTO_REUSE):
        w_embedding = tf.get_variable('word_embedding',initializer=word_vec_mat,dtype=tf.float32)
        print(word_embedding_dim)
        if add_unk_blank:
            w_embedding = tf.concat([w_embedding,
                                     tf.get_variable('unk_word_embedding',[1,word_embedding_dim],dtype = tf.float32,
                                                     initializer=tf.contrib.layers.xavier_initializer()),
                                     tf.constant(np.zeros((1,word_embedding_dim),dtype=np.float32))],0)

        x = tf.nn.embedding_lookup(w_embedding,word)

        return x


def pos_embedding(pos1,pos2,var_scope,pos_embedding_dim,max_length):
    with tf.variable_scope("position_embedding",reuse=tf.AUTO_REUSE):
        pos_tot = max_length * 2

        pos1_embedding = tf.get_variable('real_pos1_embedding',[pos_tot,pos_embedding_dim],dtype = tf.float32,initializer=tf.contrib.layers.xavier_initializer())
        pos2_embedding = tf.get_variable('real_pos2_emebdding',[pos_tot,pos_embedding_dim],dtype = tf.float32,initializer=tf.contrib.layers.xavier_initializer())
        input_pos1 = tf.nn.embedding_lookup(pos1_embedding,pos1)
        input_pos2 = tf.nn.embedding_lookup(pos2_embedding,pos2)
        x = tf.concat([input_pos1,input_pos2],-1)

        return x



def word_position_embedding(word,word_vec_mat,pos1,pos2,var_scope=None,
                            position_embedding_dim = config.model.pos_embedding_dim,max_length=config.model.max_length,add_unk_blank=True):
    word_embedding_dim = word_vec_mat.shape[1]

    w_embedding = word_embedding(word,word_vec_mat,var_scope=var_scope,word_embedding_dim=word_embedding_dim,
                                 add_unk_blank=add_unk_blank)

    p_embedding = pos_embedding(pos1,pos2,var_scope=var_scope,pos_embedding_dim=position_embedding_dim,max_length=max_length)

    x = tf.concat([w_embedding,p_embedding],-1)

    return x