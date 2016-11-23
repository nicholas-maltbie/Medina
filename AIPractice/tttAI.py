import tensorflow as tf
from ttt import *

sess = tf.InteractiveSession()

#Setup input for Tic Tac Toe
#Input is the board wrapped as a liner array in the format
#   [row1col1 row1col2 row1col3 row2col1 ... row3col3]
#
# -1 represents the enemy
#  1 represents the current player
#  0 represents empty
x = tf.placeholder(tf.int8, shape=[None, 9])
#Setup output nodes
#Each of these nodes is the ranking for the moves in the
#   different locations on the board.
y_ = tf.placeholder(tf.float32, shape=[None, 9])

#Now we must setup the variables
#Weights, 9 inputs 9 outputs
W = tf.Variable(tf.zeros([9, 9]))
#baises, 9 outputs
b = tf.Variable(tf.zeros([9]))

#now time to initialize
sess.run(tf.initialize_all_variables())
