# coding=utf-8


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from myproject import error

# ================== import data ====================#
f = open('dataset_day.csv')
df = pd.read_csv(f)  # read data
data = np.array(df['Hot'])  # get the Hot sequence
data = data[0:len(data) - 5]
# data visualization
# plt.figure()
# plt.plot(list(range(len(data))), data, color='b')
# plt.show()
mean = np.mean(data)
std = np.std(data)
normalize_data = (data - mean) / std  # normalization
# add a dimension to sequence data
normalize_data = normalize_data[:, np.newaxis]

# ==================== hyper parameters ======================#
time_step = 4
rnn_unit = 10  # hidden layer units
batch_size = 6
input_size = 1
output_size = 1
lr = 0.01  # learning rate

# ================== generate training data ===================#
train_x, train_y = [], []
for i in range(len(normalize_data) - time_step - 1):
    x = normalize_data[i:i + time_step]
    y = normalize_data[i + 1:i + time_step + 1]
    train_x.append(x.tolist())
    train_y.append(y.tolist())

# ==================== define neural network variables =====================#
X = tf.placeholder(tf.float32, [None, time_step, input_size])
Y = tf.placeholder(tf.float32, [None, time_step, output_size])
weights = {
    'in': tf.Variable(tf.random_normal([input_size, rnn_unit])),
    'out': tf.Variable(tf.random_normal([rnn_unit, 1]))
}
biases = {
    'in': tf.Variable(tf.constant(0.1, shape=[rnn_unit, ])),
    'out': tf.Variable(tf.constant(0.1, shape=[1, ]))
}


# ======================== define lstm neural network  ========================#
def lstm(batch):
    w_in = weights['in']
    b_in = biases['in']
    # We need reshape the input into two dimension tensor,
    # then put them into hidden layer.
    input = tf.reshape(X, [-1, input_size])
    input_rnn = tf.matmul(input, w_in) + b_in
    # We need reshape the two dimension tensor into three dimension tensor,
    # the put them as the input of lstm cell.
    input_rnn = tf.reshape(input_rnn, [-1, time_step, rnn_unit])
    # cell = tf.nn.rnn_cell.BasicLSTMCell(rnn_unit)
    cell = tf.nn.rnn_cell.BasicLSTMCell(rnn_unit)
    init_state = cell.zero_state(batch, dtype=tf.float32)
    # output_rnn is the result of each lstm node,
    # final_states is the result of the final cell
    output_rnn, final_states = tf.nn.dynamic_rnn(
        cell, input_rnn, initial_state=init_state, dtype=tf.float32)
    output = tf.reshape(output_rnn, [-1, rnn_unit])
    w_out = weights['out']
    b_out = biases['out']
    pred = tf.matmul(output, w_out) + b_out
    return pred, final_states


# ========================= training model ========================#
def train_lstm():
    global batch_size
    with tf.variable_scope("sec_lstm", reuse=tf.AUTO_REUSE):
        pred, _ = lstm(batch_size)
    # loss function
    loss = tf.reduce_mean(
        tf.square(tf.reshape(pred, [-1]) - tf.reshape(Y, [-1])))
    train_op = tf.train.AdamOptimizer(lr).minimize(loss)
    saver = tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        # repeat training 10000 times
        for i in range(10000):
            start = 0
            end = start + batch_size
            while (end < len(train_x)):
                _, loss_ = sess.run([train_op, loss], feed_dict={
                    X: train_x[start:end], Y: train_y[start:end]})
                start += batch_size
                end = start + batch_size
            print(i + 1, loss_)
            # save parameters every 5000 steps
            if i and (i + 1) % 5000 == 0:
                print("Save model: ", saver.save(
                    sess, './model_lstm/stock.model1', global_step=i + 1))
            if loss_ < 0.00005:
                print("Save model: ", saver.save(
                    sess, './model_lstm/stock.model1', global_step=i + 1))
                break


# ========================= prediction model ========================#
def prediction():
    with tf.variable_scope("sec_lstm", reuse=tf.AUTO_REUSE):
        # we only use one tensor [1,time_step,input_size] to test
        pred, _ = lstm(1)
    saver = tf.train.Saver(tf.global_variables())
    with tf.Session() as sess:
        try:
            # recover model
            module_file = tf.train.latest_checkpoint("./model_lstm")
            saver.restore(sess, module_file)
        except:
            # training model
            train_lstm()

        # we use the lastest data as test data。shape=[1,time_step,input_size]
        prev_seq = train_x[-1]
        predict = []
        # get the following 5 results
        for i in range(5):
            next_seq = sess.run(pred, feed_dict={X: [prev_seq]})
            predict.append(next_seq[-1])
            # Once we got the lastest prediction result,
            # we merge the prediction result and the previous data,
            # and use them as test data
            prev_seq = np.vstack((prev_seq[1:], next_seq[-1]))
        # prediction result visualization
        plt.figure()
        data = np.array(df['Hot'])
        # normalize_data_1 = (data - np.mean(data)) / np.std(data) 
        # normalize_data_1 = normalize_data_1[:, np.newaxis]
        colors = ['blue', 'red']
        label = ['data', 'predict']
        plt.plot(list(range(len(data))), data, c=colors[0], label=label[0])
        predict = np.array(predict) * std + mean
        print(predict)
        index = 0
        for item in predict:
            if item < 0:
                predict[index] = 0
            index = index + 1
        plt.plot(list(range(len(normalize_data), len(
            normalize_data) + len(predict))), predict, c=colors[1], label=label[1])
        plt.xlabel("day")  # X轴标签
        plt.ylabel("weibo amount")  # Y轴标签
        plt.title("trend predict")  # 图标题
        plt.legend(loc='best')
        plt.show()
        error.error(data[len(data) - 5:], predict)


if __name__ == '__main__':
    # train_lstm()
    prediction()
