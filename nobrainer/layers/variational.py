"""Layers for variational networks, which follow the Keras API."""

import tensorflow as tf
import tensorflow_probability as tfp


# Based on
# https://papers.nips.cc/paper/6114-weight-normalization-a-simple-reparameterization-to-accelerate-training-of-deep-neural-networks.pdf
# https://github.com/ychfan/tf_estimator_barebone/blob/master/common/layers.py
class Conv3DReparameterizationWeightNorm(tfp.layers.Convolution3DReparameterization):
    def build(self, input_shape):
        self.wn_g = self.add_weight(
            name='wn_g',
            shape=(self.filters,),
            dtype=self.dtype,
            initializer=tf.initializers.ones,
            trainable=True)
        super().build(input_shape)
        w = self.kernel_posterior.distribution.mean()
        square_sum = tf.reduce_sum(tf.square(w), [0, 1, 2, 3], keepdims=False)
        inv_norm = tf.math.rsqrt(square_sum)
        self.kernel_posterior.distribution._loc *= (inv_norm * self.wn_g)


# Based on
# https://papers.nips.cc/paper/6114-weight-normalization-a-simple-reparameterization-to-accelerate-training-of-deep-neural-networks.pdf
# https://github.com/ychfan/tf_estimator_barebone/blob/master/common/layers.py
class Conv3DFlipoutWeightNorm(tfp.layers.Convolution3DFlipout):
    def build(self, input_shape):
        self.wn_g = self.add_weight(
            name='wn_g',
            shape=(self.filters,),
            dtype=self.dtype,
            initializer=tf.initializers.ones,
            trainable=True)
        super().build(input_shape)
        w = self.kernel_posterior.distribution.mean()
        square_sum = tf.reduce_sum(tf.square(w), [0, 1, 2, 3], keepdims=False)
        inv_norm = tf.math.rsqrt(square_sum)
        self.kernel_posterior.distribution._loc *= (inv_norm * self.wn_g)
