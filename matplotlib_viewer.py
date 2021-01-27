#! /usr/bin/env python3

import matplotlib.pyplot as plt
import pickle
import sys

with open(sys.argv[1], 'rb') as f:
    fig = pickle.load(f)

fig.show()
plt.show()