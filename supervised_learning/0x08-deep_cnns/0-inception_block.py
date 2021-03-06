#!/usr/bin/env python3
"""File that contain the function inception_block"""
import tensorflow.keras as K


def inception_block(A_prev, filters):
    """
    Function that  builds an inception block as described in Going
    Deeper with Convolutions (2014)
    Args:
    A_prev is the output from the previous layer
    filters is a tuple or list containing F1, F3R, F3,F5R, F5, FPP,
    respectively:
        F1 is the number of filters in the 1x1 convolution
        F3R is the number of filters in the 1x1 convolution before the
        3x3 convolution
        F3 is the number of filters in the 3x3 convolution
        F5R is the number of filters in the 1x1 convolution before the
        5x5 convolution
        F5 is the number of filters in the 5x5 convolution
        FPP is the number of filters in the 1x1 convolution after the
        max pooling
    All convolutions inside the inception block should use a rectified
    linear activation (ReLU)
    Returns: the concatenated output of the inception block
    """
    function = 'relu'
    initializer = K.initializers.he_normal(seed=None)
    F1, F3R, F3, F5R, F5, FPP = filters

    conv1 = K.layers.Conv2D(filters=F1,
                            kernel_size=1,
                            padding='same',
                            activation=function,
                            kernel_initializer=initializer)(A_prev)

    conv2_P = K.layers.Conv2D(filters=F3R,
                              kernel_size=1,
                              padding='same',
                              activation=function,
                              kernel_initializer=initializer)(A_prev)

    conv2 = K.layers.Conv2D(filters=F3,
                            kernel_size=3,
                            padding='same',
                            activation=function,
                            kernel_initializer=initializer)(conv2_P)

    conv3_p = K.layers.Conv2D(filters=F5R,
                              kernel_size=1,
                              padding='same',
                              activation=function,
                              kernel_initializer=initializer)(A_prev)

    conv3 = K.layers.Conv2D(filters=F5,
                            kernel_size=5,
                            padding='same',
                            activation=function,
                            kernel_initializer=initializer)(conv3_p)

    layer_pool = K.layers.MaxPooling2D(pool_size=[3, 3],
                                       strides=(1, 1),
                                       padding='same')(A_prev)

    layer_poolP = K.layers.Conv2D(filters=FPP,
                                  kernel_size=1,
                                  padding='same',
                                  activation=function,
                                  kernel_initializer=initializer)(layer_pool)

    mid_layer = K.layers.concatenate([conv1, conv2, conv3, layer_poolP])

    return mid_layer
