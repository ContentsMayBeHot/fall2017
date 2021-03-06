"""logistic.py

Author: Rei Armenia, Matthew James Harrison
Class: CSI-480 AI
Assignment: Supervised Learning Programming Assignment
Due Date: November 28, 2017

Description:
Which digit? Which action?

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
 - Reproduce this assignment and provide a copy to another member of academic
   staff; and/or
 - Communicate a copy of this assignment to a plagiarism checking service
   (which may then retain a copy of this assignment on its database for the
   purpose of future plagiarism checking)

----------------------
Champlain College CSI-480, Fall 2017
The following code was adapted by Joshua Auerbach (jauerbach@champlain.edu)
from the UC Berkeley Pacman Projects (see license and attribution below).

----------------------
Licensing Information:  You are free to use or extend these projects for
educational purposes provided that (1) you do not distribute or publish
solutions, (2) you retain this notice, and (3) you provide clear
attribution to UC Berkeley, including a link to http://ai.berkeley.edu.

Attribution Information: The Pacman AI projects were developed at UC Berkeley.
The core projects and autograders were primarily created by John DeNero
(denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
Student side autograding was added by Brad Miller, Nick Hay, and
Pieter Abbeel (pabbeel@cs.berkeley.edu).
"""


# Perceptron implementation
import util
PRINT = True

import numpy as np
import tensorflow as tf

class SoftmaxClassifier:
    """
    A softmax (multinomial logistic regression) classifier.

    This Class will perform softmax classification using TensorFlow

    Note that the variable 'datum' in this code refers to a counter of features
    """
    def __init__( self, legal_labels, max_iterations):
        self.legal_labels = legal_labels
        self.type = "logistic"
        self.max_iterations = max_iterations
        self.learning_rates = [0.2]

        # create TensorFlow session
        self.sess = tf.InteractiveSession()


    def train( self, training_data, training_labels, validation_data, validation_labels ):
        """
        The training loop for the softmax classifier passes through the training data several
        times and updates the weight vector for each label based on the cross entropy loss

        You will need to setup tensor flow variables, computation graph,
        and optimization procedure, then run the training step self.max_iterations
        times.

        This should be very similar to what is shown
           https://www.tensorflow.org/get_started/mnist/beginners
        except for where the data is coming from

        Important note: this should operate in batch mode, using all training_data
            for each batch
        """

        self.features = list(training_data[0].keys()) # could be useful later

        learning_rate = self.learning_rates[0]

        # Note: features should come into tf.placeholder self.x and output
        # should be in self.y to make the classify method work correctly.
        # If you use different variable names, then you will need to change
        # that method accordingly

        "*** YOUR CODE HERE ***"
        results = []
        for lr in self.learning_rates:
            batch_size = len(training_labels)
            batch_xs = np.asarray(
                [datum.values_as_numpy_array() for datum in training_data]
            )
            batch_ys = np.zeros((batch_size, 10))
            batch_ys[np.arange(batch_size), training_labels] = 1
            # Source: https://stackoverflow.com/a/29831596

            self.x = tf.placeholder(tf.float32, [None, 784])
            W = tf.Variable(tf.zeros([784, 10]))
            b = tf.Variable(tf.zeros([10]))
            y = tf.nn.softmax(tf.matmul(self.x, W) + b)

            y_ = tf.placeholder(tf.float32, [None, 10])
            cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
            train_step = tf.train.GradientDescentOptimizer(lr).minimize(cross_entropy)

            tf.global_variables_initializer().run()

            for _ in range(self.max_iterations):
                self.sess.run(train_step, feed_dict={self.x: batch_xs, y_: batch_ys})
            self.y = y

            correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
            accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
            a = self.sess.run(accuracy, feed_dict={self.x: batch_xs, y_: batch_ys})
            results.append((lr, a))
        best_lr = max(results, key=lambda x: x[1])[0]

        train_step = tf.train.GradientDescentOptimizer(best_lr).minimize(cross_entropy)
        for _ in range(self.max_iterations):
            self.sess.run(train_step, feed_dict={self.x: batch_xs, y_: batch_ys})
        self.y = y

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """

        output = tf.argmax(self.y,1)
        return self.sess.run(output, feed_dict={self.x: [datum.values_as_numpy_array() for datum in data]})




    def find_high_weight_features(self, label, num=100):
        """
        Returns a list of the num features with the greatest weight for some label
        """

        # this function is optional for this classifier, but if you want to
        # visualize the weights of this classifier, you will need to implement
        # it

        util.raise_not_defined()
