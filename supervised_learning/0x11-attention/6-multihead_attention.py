#!/usr/bin/env python3
"""File that conatins the class MultiHeadAttention"""
import tensorflow as tf
sdp_attention = __import__('5-sdp_attention').sdp_attention


class MultiHeadAttention(tf.keras.layers.Layer):
    """Class that perform multi head attention"""

    def __init__(self, dm, h):
        """
        Class constructor
          dm is an integer representing the dimensionality of the model
          h is an integer representing the number of heads
          dm is divisible by h
        Sets the following public instance attributes:
          h - the number of heads
          dm - the dimensionality of the model
          depth - the depth of each attention head
          Wq - a Dense layer with dm units, used to generate the query matrix
          Wk - a Dense layer with dm units, used to generate the key matrix
          Wv - a Dense layer with dm units, used to generate the value matrix
          linear - a Dense layer with dm units, used to generate the attention
          output
        """
        self.h = h
        self.dm = dm
        self.depth = dm // h

        self.Wq = tf.keras.layers.Dense(units=dm)
        self.Wk = tf.keras.layers.Dense(units=dm)
        self.Wv = tf.keras.layers.Dense(units=dm)

        self.linear = tf.keras.layers.Dense(units=dm)

        super(MultiHeadAttention, self).__init__()

    def call(self, Q, K, V, mask):
        """
        Publci instance method
        Args:
          Q is a tensor of shape (batch, seq_len_q, dk) containing the input to
          generate the query matrix
          K is a tensor of shape (batch, seq_len_v, dk) containing the input to
          generate the key matrix
          V is a tensor of shape (batch, seq_len_v, dv) containing the input to
          generate the value matrix
          mask is always None
        Returns: output, weights
          outputa tensor with its last two dimensions as (..., seq_len_q, dm)
          containing the scaled dot product attention
          weights a tensor with its last three dimensions as
          (..., h, seq_len_q, seq_len_v) containing the attention weights
        """
        def split_heads(x, batch_size):
            """Split the last dimension into (num_heads, depth).
            Transpose the result such that the shape is (batch_size,
            num_heads, seq_len, depth)"""
            x = tf.reshape(x, (batch_size, -1, self.h, self.depth))
            return tf.transpose(x, perm=[0, 2, 1, 3])

        batch_size = tf.shape(Q)[0]

        q = self.Wq(Q)  # (batch_size, seq_len, d_model)
        k = self.Wk(K)  # (batch_size, seq_len, d_model)
        v = self.Wv(V)  # (batch_size, seq_len, d_model)

        q = split_heads(q, batch_size)
        k = split_heads(k, batch_size)
        v = split_heads(v, batch_size)

        scaled_attention, attention_weights = sdp_attention(q, k, v, mask)

        scaled_attention = tf.transpose(scaled_attention,
                                        perm=[0, 2, 1, 3])

        concat_attention = tf.reshape(scaled_attention, (batch_size, -1,
                                                         self.dm))

        output = self.linear(concat_attention)
        return output, attention_weights
