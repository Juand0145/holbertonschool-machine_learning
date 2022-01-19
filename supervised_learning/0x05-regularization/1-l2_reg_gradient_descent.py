#!/usr/bin/env python3
"""File That contains the function l2_reg_gradient_descent"""
import numpy as np


def l2_reg_gradient_descent(Y, weights, cache, alpha, lambtha, L):
    """
    Function that calculates  updates the weights and biases of a neural
    network using gradient descent with L2 regularization:
    Args:
    Y is a one-hot numpy.ndarray of shape (classes, m) that contains the
    correct labels for the data
        classes is the number of classes
        m is the number of data points
    weights is a dictionary of the weights and biases of the neural network
    cache is a dictionary of the outputs of each layer of the neural network
    alpha is the learning rate
    lambtha is the L2 regularization parameter
    L is the number of layers of the network
    """
    m = Y.shape[1]
    Layers = range(L + 1)[1:L + 1]

    for i in reversed(Layers):
        A = cache["A{}".format(i)]

        if i == L:
            dZ = cache["A{}".format(i)] - Y
            dW = (np.matmul(cache["A{}".format(i - 1)], dZ.T) / m).T

            dW_L2 = dW + (lambtha / m) * weights["W{}".format(i)]
            db = np.sum(dZ, axis=1, keepdims=True) / m

        else:
            dW2 = np.matmul(weights["W{}".format(i + 1)].T, dZ2)
            tanh = 1 - (A * A)
            dZ = dW2 * tanh
            dW = np.matmul(dZ, cache["A{}".format(i - 1)].T) / m

            dW_L2 = dW + (lambtha / m) * weights["W{}".format(i)]
            db = np.sum(dZ, axis=1, keepdims=True) / m

        weights["W{}".format(i)] = (weights["W{}".format(i)]) - (alpha * dW_L2)
        weights["b{}".format(i)] = weights["b{}".format(i)] - (alpha * db)
        dZ2 = dZ