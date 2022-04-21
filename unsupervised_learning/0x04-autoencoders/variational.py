#!/usr/bin/env python3
"""File that contains the function autoencoder"""
import tensorflow.keras as keras


def autoencoder(input_dims, hidden_layers, latent_dims):
    """
    Function that creates a variational autoencoder
    Args:
      input_dims is an integer containing the dimensions of the model input
      hidden_layers is a list containing the number of nodes for each hidden
      layer in the encoder, respectively
        the hidden layers should be reversed for the decoder
      latent_dims is an integer containing the dimensions of the latent space
      representation
    Returns: encoder, decoder, auto
      encoder is the encoder model, which should output the latent
      representation, the mean, and the log variance, respectively
      decoder is the decoder model
      auto is the full autoencoder model
    """
    # Encoder
    input_encoder = keras.Input(shape=(input_dims, ))

    prev_layer = input_encoder
    number_layers = len(hidden_layers)
    for i in range(number_layers):
        hidden_layer = keras.layers.Dense(units=hidden_layers[i],
                                          activation="relu")

        prev_layer = hidden_layer(prev_layer)

    # Encoder sampling = https://towardsdatascience.com/intuitively-
    # understanding-variational-autoencoders-1bfe67eb5daf
    mean = keras.layers.Dense(units=latent_dims, activation=None)
    log_sigma = keras.layers.Dense(units=latent_dims, activation=None)

    def sampling(args):
        """Sampling similar points in latent space"""
        z_m, z_stand_des = args
        batch = keras.backend.shape(z_m)[0]
        dim = keras.backend.int_shape(z_m)[1]
        epsilon = keras.backend.random_normal(shape=(batch, dim))
        return z_m + keras.backend.exp(z_stand_des / 2) * epsilon

    z = keras.layers.Lambda(sampling,
                            output_shape=(latent_dims,))([mean,
                                                          log_sigma])
    encoder = keras.Model(input_encoder, [z, mean, log_sigma])

    # Decoder
    input_decoder = keras.Input(shape=(latent_dims,))

    prev_later = input_decoder
    for i in range(number_layers - 1, -1, -1):
        hidden_layer = keras.layers.Dense(units=hidden_layers[i],
                                          activation='relu')
        prev_layer = hidden_layer(prev_later)

    output_layer = keras.layers.Dense(units=input_dims,
                                      activation='sigmoid')

    decoder_outputs = output_layer(prev_layer)

    decoder = keras.Model(inputs=input_decoder,
                          outputs=decoder_outputs)

    # Autoencoder
    e_output = encoder(input_encoder)[-1]
    d_output = decoder(e_output)
    auto = keras.Model(input_encoder, d_output)

    def vae_loss(x, x_decoder_mean):
        x_loss = keras.backend.binary_crossentropy(x, x_decoder_mean)
        x_loss = keras.backend.sum(x_loss, axis=1)
        kl_loss = - 0.5 * keras.backend.mean(1 + log_sigma -
                                             keras.backend.square(mean) -
                                             keras.backend.exp(log_sigma),
                                             axis=-1)
        return x_loss + kl_loss

    auto.compile(loss=vae_loss, optimizer='adam')

    return encoder, decoder, auto
