#! /usr/bin/env python3

import matplotlib.pyplot as plt
import pickle
import sys
import glob
import os


def press(event):
    global current_index
    print('press')

    if event.key == 'left':
        current_index -= 1
    elif event.key == 'right':
        current_index += 1
    else:
        return

    display(figure_files[current_index % len(figure_files)])


def display(figure_file):
    old_fig = plt.gcf()
    geometry = plt.get_current_fig_manager().window.geometry()

    with open(figure_file, 'rb') as f:
        fig = pickle.load(f)

    fig.show()
    plt.get_current_fig_manager().window.setGeometry(geometry)
    plt.close(old_fig)
    plt.gcf().canvas.mpl_connect('key_press_event', press)


file_to_open = sys.argv[1]

working_dir = os.path.dirname(file_to_open)
figure_files = glob.glob(os.path.join(os.path.abspath(working_dir), '*.mplf'))

current_index = figure_files.index(file_to_open)

display(file_to_open)
plt.show()
