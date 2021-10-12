# -*- coding: utf-8 -*-
"""time_series_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1j5zgsqdEvlc-wRq6JnimhVEuBy2DQY59
"""

from numpy import array
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd

def split_sequence(sequence, n_steps):
    X, y = list(), list()
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence)-1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)

# Loading data
df = pd.read_csv('co2data.csv')
df.columns = ['X', 'y']
df['X'] = pd.to_datetime(df["X"], format='%Y-%m-%d %H:%M:%S')
df['y'] = pd.to_numeric(df.y.str.replace('ppm', ''), downcast='float')
df.set_index('X')
raw_seq = df['y'].values.tolist()
# choose a number of time steps
n_steps = 5
# split into samples
X, y = split_sequence(raw_seq, n_steps)
# summarize the data

# define model
model = Sequential()
model.add(Dense(100, activation= 'relu' , input_dim=n_steps))
model.add(Dense(1))
model.compile(optimizer= 'adam' , loss=  'mse' )

# fit model
model.fit(X, y, epochs=2000, verbose=0)

# demonstrate prediction
x_input = array([449.01998901, 449.66000366, 451.38000488, 451.10998535, 449.79000854])
x_input = x_input.reshape((1, n_steps))
yhat = model.predict(x_input, verbose=0)
print(yhat)